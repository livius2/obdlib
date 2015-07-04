import unittest
import utils


class TestUtils(unittest.TestCase):
    def setUp(self):
        utils.unit_english = 0

    def test_rpm(self):
        assert utils.rpm('0000') == 0.0
        assert utils.rpm('FFFF') == 16383.75

    def test_speed(self):
        # unit_english == 0
        assert utils.speed('00') == 0.0
        assert utils.speed('FF') == 255

        # unit_english == 1
        utils.unit_english = 1
        assert utils.speed('00') == 0.0
        assert utils.speed('FF') == 158.44965396

    def test_load_value(self):
        self.assertEqual(utils.load_value('00'), 0)
        self.assertEqual(utils.load_value('FF'), 100)

    def test_term_fuel(self):
        self.assertEqual(utils.term_fuel('00'), -100)
        self.assertEqual(utils.term_fuel('FF'), 99.22)

    def test_fuel_pressure(self):
        # unit_english == 0
        self.assertEqual(utils.fuel_pressure('00'), 0)
        self.assertEqual(utils.fuel_pressure('FF'), 765)
        # unit_english == 1
        utils.unit_english = 1
        self.assertEqual(utils.fuel_pressure('00'), 0)
        self.assertEqual(utils.fuel_pressure('FF'), 110.95)

    def test_absolute_pressure(self):
        # unit_english == 0
        self.assertEqual(utils.absolute_pressure('00'), 0)
        self.assertEqual(utils.absolute_pressure('FF'), 255)

        # unit_english == 1
        utils.unit_english = 1
        self.assertEqual(utils.absolute_pressure('00'), 0)
        self.assertEqual(utils.absolute_pressure('FF'), 36.98)

    def test_timing_advance(self):
        self.assertEqual(utils.timing_advance('00'), -64)
        self.assertEqual(utils.timing_advance('FF'), 63.5)

    def test_air_flow_rate(self):
        self.assertEqual(utils.air_flow_rate('0000'), 0)
        self.assertEqual(utils.air_flow_rate('FFFF'), 655.35)

    def test_throttle_pos(self):
        self.assertEqual(utils.throttle_pos('00'), 0)
        self.assertEqual(utils.throttle_pos('FF'), 100)

    def test_air_status(self):
        self.assertIsNone(utils.air_status('00'))
        self.assertEqual(utils.air_status('01'), 'Upstream')
        self.assertEqual(utils.air_status('02'), 'Downstream of catalytic converter')
        self.assertEqual(utils.air_status('04'), 'From the outside atmosphere or off')
        self.assertEqual(utils.air_status('08'), 'Pump commanded on for diagnostics')

    def test_voltage(self):
        self.assertEqual(utils.voltage('00'), 0)
        self.assertEqual(utils.voltage('FF'), 1.275)

    def test_coolant_temp(self):
        self.assertEqual(utils.coolant_temp('00'), -40)
        self.assertEqual(utils.coolant_temp('FF'), 215)

        # unit_english == 1
        utils.unit_english = 1
        self.assertEqual(utils.coolant_temp('00'), -40)
        self.assertEqual(utils.coolant_temp('FF'), 419.0)

    def test_obd_standards(self):
        self.assertEqual(utils.obd_standards('FF'), None)
        self.assertEqual(utils.obd_standards('01'), 'OBD-II as defined by the CARB')

    def test_time(self):
        self.assertEqual(utils.time('0000'), 0)
        self.assertEqual(utils.time('FFFF'), 65535)

    def test_oil_temp(self):
        self.assertEqual(utils.oil_temp('00'), -40)
        self.assertEqual(utils.oil_temp('FF'), 215)

        # unit_english == 1
        utils.unit_english = 1
        self.assertEqual(utils.oil_temp('00'), -40)
        self.assertEqual(utils.oil_temp('FF'), 419.0)

    def test_fuel_type(self):
        self.assertEqual(utils.fuel_type('00'), 'Not Available')
        self.assertEqual(utils.fuel_type('05'), 'Liquefied petroleum gas (LPG)')
        self.assertEqual(utils.fuel_type('FF'), None)

    def test_bitwise_pids(self):
        """
            Verify we correctly parse information about supported PIDs on a 1999
            Dodge Durango
        """
        durango_supported_pids = 'BE3EB810'
        supported_pids = utils.bitwise_pids(durango_supported_pids)
        assert supported_pids == {
            '01': True,
            '02': False,
            '03': True,
            '04': True,
            '05': True,
            '06': True,
            '07': True,
            '08': False,
            '09': False,
            '0A': False,
            '0B': True,
            '0C': True,
            '0D': True,
            '0E': True,
            '0F': True,
            '10': False,
            '11': True,
            '12': False,
            '13': True,
            '14': True,
            '15': True,
            '16': False,
            '17': False,
            '18': False,
            '19': False,
            '1A': False,
            '1B': False,
            '1C': True,
            '1D': False,
            '1E': False,
            '1F': False,
            '20': False
        }


suite = unittest.TestLoader().loadTestsFromTestCase(TestUtils)
unittest.TextTestRunner(verbosity=2).run(suite)
