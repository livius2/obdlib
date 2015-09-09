from time import sleep
import obdlib.uart as uart
import obdlib.elm327 as elm327
from obdlib.response import Response
from obdlib.logging import logger


class Scanner(object):
    """
        ELM327 OBD-II Scanner

        Information about OBD-II PIDs
        http://en.wikipedia.org/wiki/OBD-II_PIDs

        Additional details about EML327 OBD <-> RS232 found here:
        http://elmelectronics.com/DSheets/ELM327DS.pdf
    """

    def __init__(self, pb_str, baud=uart.DEFAULT_BAUDRATE, units=0):
        """
            Init params
            :param pb_str: port or bus number|name
            :param baud: it is the clock rate
            :param units: default units for system readings
            (0 - Europe, 1 - English)
        """
        self.pb_str = pb_str
        self.baud = baud
        self.uart_port = None
        self.elm_version = ""
        self.obd_protocol = ""
        self.units = units
        self.success = "OK"
        self.sensor = None
        # it does prove that the connection with a vehicle is working
        self.connected = False

    def connect(self):
        """
            Opens a connection to an ELM327 OBD-II Interface
            :return:
        """
        self.uart_port = uart.UART().connection(
            self.pb_str,
            baudrate=self.baud)

        if self.is_port():
            self.initialize()

    def is_port(self):
        """ Returns a boolean for whether a successful connection
            with port was made
        """
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

    def disconnect(self):
        """
            Disconnect from a connected OBD-II Scanner
            :return:
        """
        if self.is_port():
            self.reset()
            self.uart_port.close()
        self.connected = None
        self.elm_version = ""

    def initialize(self):
        """
            Initialize the OBD-II Scanner state after connecting
            :return:
        """
        self.reset()
        self.check_echo_off()
        self.check_spaces_off()
        self.check_feed_off()

        # Disable memory function
        self.send(elm327.MEMORY_OFF_COMMAND)

        self.set_protocol()
        self.header_on()
        self.set_sensors()

    def set_sensors(self):
        raise NotImplementedError()

    def check_connection(self):
        if not self.connected:
            mess = "Failed connection to the OBD2 interface!"
            logger.error(mess)
            raise Exception(mess)

    def header_on(self):
        if not self._check_response(
                self.send(elm327.HEADER_ON_COMMAND).raw_value):
            mess = "Enable header command did not completed"
            logger.error(mess)
            raise Exception(mess)

    def echo_off(self):
        """
            Turns ECHO OFF for the OBD-II Scanner
            :return response data
        """
        return self.send(elm327.ECHO_OFF_COMMAND).raw_value

    def set_protocol(self):
        if not self._check_response(
                self.send(elm327.SET_PROTOCOL_AUTO_COMMAND).raw_value):
            mess = "Set protocol command did not completed"
            logger.error(mess)
            raise Exception(mess)

    def check_echo_off(self):
        if not self._check_response(self.echo_off()):
            mess = "Echo command did not completed"
            logger.error(mess)
            raise Exception(mess)

    def check_spaces_off(self):
        if not self._check_response(
                self.send(elm327.SPACES_OFF_COMMAND).raw_value):
            logger.warning("Spaces off command did not completed")

    def check_feed_off(self):
        if not self._check_response(
                self.send(elm327.LINEFEED_OFF_COMMAND).raw_value):
            logger.warning("Line feed off command did not completed")

    def get_proto_num(self):
        """
            Retrieves the protocol number (response format is - A4)
        """
        number = self.obd_protocol
        if len(number) == 2 and 'A' in number:
            number = int(number[-1], 16)

        return number if number else 0

    def reset(self):
        """
            Reset the OBD-II Scanner
            :return:
        """
        if self.is_port():
            self.elm_version = self.send(elm327.RESET_COMMAND, 1).at_value

    def receive(self):
        """
            Receive data from connected OBD-II Scanner
            :return: the data returned by the OBD-II Scanner
        """
        if self.is_port():
            value = self.collect_data()
            if value:
                return Response(value, self.get_proto_num())
        else:
            mess = "Cannot read when unconnected"
            logger.error(mess)
            raise Exception(mess)

        return Response()

    def collect_data(self):
        """
            Listens an UART port and
            retrieves data from one
        """
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
        return value

    def send(self, data, wait=None):
        """
            Send data/command to the connected OBD-II Scanner
            :param data: the data/command to send to the connected OBD-II
            scanner
            :param wait: the delay between write and read, in sec
            :return the data returned by the OBD-II Scanner
        """
        if self.is_port():
            self._write(data)

        # Wait for data to become available
        if wait:
            sleep(wait)

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
        cmd = data + "\r\n"
        self.uart_port.write(cmd.encode())
