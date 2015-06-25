import time
import uart
import elm327
import decode
from obd import commands
from obd import sensors
from response import Response
from obd.fuel_type import FUEL_TYPE_DESCRIPTION


class OBDScanner(object):
    """
        ELM327 OBD-II Scanner

        Information about OBD-II PIDs
        http://en.wikipedia.org/wiki/OBD-II_PIDs

        Additional details about EML327 OBD <-> RS232 found here:
        http://elmelectronics.com/DSheets/ELM327DS.pdf
    """

    def __init__(self, pb_str, baud=uart.DEFAULT_BAUDRATE):
        self.pb_str = pb_str
        self.baud = baud
        self.uart_port = None
        self.elm_version = ""
        self.obd_protocol = ""
        # Time to wait (in seconds) before attempting to receive data after an
        # OBD command has been issued
        self.receive_wait_time = 0.5
        self.success = "OK"
        # the data object returned by the OBD-II Scanner
        self.__response = None
        self.sensor = None

    def connect(self):
        """
            Opens a connection to an ELM327 OBD-II Interface
            :return:
        """
        self.uart_port = uart.UART().connection(self.pb_str, baudrate=self.baud)

        if self.is_connected():
            self.initialize()

    def is_connected(self):
        """ Returns a boolean for whether a successful connection was made """
        return self.uart_port is not None

    def __enter__(self):
        """
            Sets up the OBDScanner to work as a ContextManager
            :return: this OBDScanner instance for use within the context
        """
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def battery_voltage(self):
        """
            Reads the vehicle's battery voltage from a connected OBD-II Scanner
            :return: the battery voltage returned by the OBD-II Scanner
        """
        self.send(elm327.BATTERY_VOLTAGE_COMMAND)
        return self.receive()

    def clear_trouble_codes(self):
        """
            Uses OBD Mode 04 to clear trouble codes and the malfunction
            indicator lamp (MIL) / check engine light
            :return:
        """
        self.send(commands.CLEAR_TROUBLE_CODES_COMMAND)

    def current_engine_coolant_temperature(self):
        """
            Reads the vehicle's current engine coolant temperature from a
            connected OBD-II Scanner
            :return: the current engine coolant temperature in degrees Celsius
        """
        self.send(commands.CURRENT_ENGINE_COOLANT_TEMP_COMMAND)
        response = self.receive()
        response_data = response.strip().split(' ')[-1]
        # The data returned in the OBD response is in hexadecimal with a zero
        # offset to account for negative temperatures. To return the current
        # temperature in degrees Celsius, we must first convert to decimal and
        # then subtract 40 to account for the zero offset.
        return int(response_data, 16) - 40

    def current_engine_oil_temperature(self):
        """
            Reads the vehicle's current engine oil temperature from a connected
            OBD-II Scanner
            :return: the current engine oil temperature in degrees Celsius
        """
        self.send(commands.CURRENT_ENGINE_OIL_TEMP_COMMAND)
        response = self.receive()
        response_data = response.strip().split(' ')[-1]
        # The data returned in the OBD response is in hexadecimal with a zero
        # offset to account for negative temperatures. To return the current
        # temperature in degrees Celsius, we must first convert to decimal and
        # then subtract 40 to account for the zero offset.
        return int(response_data, 16) - 40

    def ecu_name(self):
        """
            Returns the name of the Engine Control Unit (ECU)
            :return: the name of the ECU (if available)
        """
        return self.send(commands.ECU_NAME_COMMAND)

    def fuel_type(self):
        """
            Reads the vehicle's fuel type from a connected OBD-II Scanner
            :return: a description of the type of fuel used by the vehicle
        """
        self.send(commands.FUEL_TYPE_COMMAND)
        response = self.receive()
        response_data = response.strip().split(' ')[-1]
        return FUEL_TYPE_DESCRIPTION.get(int(response_data, 16))

    def echo_off(self):
        """
            Turns ECHO OFF for the OBD-II Scanner
            :return response data
        """
        return self.send(elm327.ECHO_OFF_COMMAND).raw_value

    def disconnect(self):
        """
            Disconnect from a connected OBD-II Scanner
            :return:
        """
        if self.is_connected():
            self.reset()
            self.uart_port.close()
        self.uart_port = None
        self.elm_version = ""

    def initialize(self):
        """
            Initialize the OBD-II Scanner state after connecting
            :return:
        """
        # self.reset()
        if not self._check_response(self.echo_off()):
            # logging error
            print("ATE0 did not return success")
        if not self._check_response(self.send(elm327.SET_PROTOCOL_AUTO_COMMAND).raw_value):
            # logging error
            print("ATE0 did not return success")
        self.obd_protocol = self.send(elm327.DESCRIBE_PROTOCOL_COMMAND).raw_value
        self.sensor = sensors.Command(self.send)

    def receive(self):
        """
            Receive data from connected OBD-II Scanner
            :return: the data returned by the OBD-II Scanner
        """
        if self.is_connected():
            retry_number = 0
            value = b''
            while True:
                data = self.uart_port.read(1)

                if data == b'>':
                    break

                # ignore incoming bytes that are of value 00 (NULL)
                if data == b'\x00':
                    continue

                if len(data) == 0:
                    if retry_number >= elm327.DEFAULT_RETRIES:
                        break
                    retry_number += 1
                    continue

                value += data

            if value:
                return Response(value)
        else:
            # logging warning
            print "Cannot read when unconnected"

        return None

    def reset(self):
        """
            Reset the OBD-II Scanner
            :return:
        """
        if self.is_connected():
            self.send(elm327.RESET_COMMAND, 1)
            self.elm_version = self.receive()

    def send(self, data, delay=None):
        """
            Send data/command to the connected OBD-II Scanner
            :param data: the data/command to send to the connected OBD-II
            scanner
            :param delay: the delay between write and read, in sec
            :return the data returned by the OBD-II Scanner
        """
        if self.is_connected():
            self._write(data)

        # Wait for data to become available
        if delay:
            time.sleep(delay)

        return self.receive()

    def supported_pids(self):
        response = self.send(commands.CURRENT_MODE_PIDS_SUPPORTED_COMMAND)
        return decode.decode_bitwise_pids(response.value)

    def vehicle_id_number(self):
        """
            Returns the vehicle's identification number (VIN)
            :return:
        """
        self.send(commands.VEHICLE_ID_NUMBER_COMMAND)
        return self.receive()

    def _check_response(self, data):
        """
            Checks the common command
        """
        return self.success in data

    def _write(self, data):
        """
            Send data/command to the connected OBD-II Scanner
            :param data: the data/command to send to the connected OBD-II
            scanner
            :return:
        """
        self.uart_port.flushOutput()
        self.uart_port.flushInput()
        self.uart_port.write(data + "\r\n")