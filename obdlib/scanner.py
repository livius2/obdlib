import obdlib.elm327 as elm327
from obdlib.obd import commands
from obdlib.obd import sensors
from obdlib.logging import logger
from obdlib.obdscan import Scanner


class OBDScanner(Scanner):
    def __init__(self, *args, **kwargs):
        Scanner.__init__(self, *args, **kwargs)

    def set_sensors(self):
        self.sensor = sensors.Command(self.send, self.units)
        # checks connection with vehicle
        self.connected = self.sensor.check_pids()

        self.check_connection()

        self.obd_protocol = self.send(
            elm327.DESCRIBE_PROTOCOL_NUMBER_COMMAND).at_value

        # gets available pids
        self.sensor.check_pids()

    def vehicle_id_number(self):
        """
            Returns the vehicle's identification number (VIN)
            :return dict {ecu: number}
        """
        sensor = self.sensor[9]('02')
        vin = {}
        for ecu, value in sensor.ecus:
            vin[ecu] = value
        return vin

    def battery_voltage(self):
        """
            Reads the vehicle's battery voltage from a connected OBD-II Scanner
            :return: the battery voltage returned by the OBD-II Scanner
        """
        return self.send(elm327.BATTERY_VOLTAGE_COMMAND).at_value

    def get_basic_info(self):
        """
            Returns general vehicle's information
            :return dict
        """
        gen_info = {}

        # complies with OBD std
        sensor = self.sensor[1]('1C')
        obd = {}
        for ecu, value in sensor.ecus:
            obd[ecu] = value
        gen_info[sensor.title] = obd

        # fuel type
        sensor = self.sensor[1]('51')
        f_type = {}
        for ecu, value in sensor.ecus:
            f_type[ecu] = value
        if f_type:
            gen_info[sensor.title] = f_type

        # get VIN
        gen_info['VIN'] = self.vehicle_id_number()

        # battery voltage
        gen_info['BATTERY_VOLTAGE'] = self.battery_voltage()

        return gen_info

    def clear_trouble_codes(self):
        """
            Uses OBD Mode 04 to clear trouble codes and the malfunction
            indicator lamp (MIL) / check engine light
            :return:
        """
        if not self._check_response(
                self.send(commands.CLEAR_TROUBLE_CODES_COMMAND).raw_value):
            # logging warning
            logger.warning("Clear trouble codes did not return success")


