import unittest
import sys

if sys.version_info[0] < 3:
    import mock
else:
    import unittest.mock as mock

import obdlib.scanner as scanner


class TestOBDScanner(unittest.TestCase):
    def setUp(self):
        self.scan = scanner.OBDScanner("/dev/null")

    @mock.patch('obdlib.scanner.OBDScanner.is_port')
    @mock.patch('obdlib.scanner.OBDScanner.initialize')
    @mock.patch('obdlib.uart.UART.connection')
    def test_connection(self, mock_uart, mock_init, mock_is_port):
        mock_is_port.return_value = True
        self.scan.connect()
        self.assertEqual(mock_init.call_count, 1)
        self.assertEqual(mock_uart.call_count, 1)
        self.assertEqual(mock_init.call_args_list[0][0], ())
        self.assertEqual(mock_uart.call_args_list[0][0], ('/dev/null',))
        self.assertEqual(mock_uart.call_args_list[0][1], {'baudrate': 38400})

    def test_is_port(self):
        # False
        self.scan.uart_port = None
        is_port = self.scan.is_port()
        self.assertFalse(is_port)
        # True
        self.scan.uart_port = object
        is_port = self.scan.is_port()
        self.assertTrue(is_port)

    @mock.patch('obdlib.scanner.OBDScanner.vehicle_id_number')
    @mock.patch('obdlib.scanner.OBDScanner.battery_voltage')
    def test_get_basic_info(self, mock_voltage, mock_vin):
        mock_vin.return_value = {'E8': '2312KJLKJHLKJ43L34323'}
        mock_voltage.return_value = 12.7
        self.scan.sensor = mock.MagicMock()

        class p(object):
            def __init__(self, n):
                if int(n, 16) == 28:
                    self.values = {'E8': 'OBD and OBD-II'}
                if int(n, 16) == 81:
                    self.values = {'E8': 'Gasoline'}

            @property
            def gen(self):
                for ecu, value in self.values.items():
                    yield (ecu, value)

        def mode(a):
            def pid(n):
                pid.ecus = p(n).gen
                if int(n, 16) == 28:
                    pid.title = 'OBD'
                if int(n, 16) == 81:
                    pid.title = 'FUEL_TYPE'
                return pid

            return pid

        self.scan.sensor.__getitem__.side_effect = mode
        info = self.scan.get_basic_info()
        self.assertEqual(mock_vin.call_count, 1)
        self.assertEqual(mock_vin.call_args_list[0][0], ())
        self.assertEqual(info,
                         {
                             'BATTERY_VOLTAGE': 12.7,
                             'OBD': {'E8': 'OBD and OBD-II'},
                             'VIN': {'E8': '2312KJLKJHLKJ43L34323'},
                             'FUEL_TYPE': {'E8': 'Gasoline'}
                         })

    @mock.patch('obdlib.scanner.OBDScanner.send')
    def test_battery_voltage(self, mock_send):
        volt = self.scan.battery_voltage()
        self.assertEqual(mock_send.call_count, 1)
        self.assertEqual(mock_send.call_args_list[0][0], ('ATRV',))

    @mock.patch('obdlib.scanner.OBDScanner.reset')
    @mock.patch('obdlib.scanner.OBDScanner.is_port')
    def test_disconnect(self, mock_is_port, mock_reset):
        # is_port True
        mock_is_port.return_value = True
        self.scan.uart_port = mock.Mock()
        self.scan.disconnect()
        self.assertEqual(mock_is_port.call_count, 1)
        self.assertEqual(mock_is_port.call_args_list[0][0], ())
        self.assertEqual(mock_reset.call_count, 1)
        self.assertEqual(mock_reset.call_args_list[0][0], ())
        self.assertEqual(self.scan.uart_port.close.call_count, 1)
        self.assertEqual(self.scan.uart_port.close.call_args_list[0][0], ())
        # is_port False
        mock_is_port.reset_mock()
        mock_reset.reset_mock()
        self.scan.uart_port.reset_mock()
        mock_is_port.return_value = False
        self.scan.disconnect()
        self.assertEqual(mock_is_port.call_count, 1)
        self.assertEqual(mock_is_port.call_args_list[0][0], ())
        self.assertEqual(mock_reset.call_count, 0)
        self.assertEqual(self.scan.uart_port.close.call_count, 0)

    @mock.patch('sys.stdout')
    @mock.patch('obdlib.scanner.sensors.Command')
    @mock.patch('obdlib.scanner.OBDScanner.send')
    @mock.patch('obdlib.scanner.OBDScanner.echo_off')
    @mock.patch('obdlib.scanner.OBDScanner.reset')
    def test_initialize(self, mock_reset, mock_echo, mock_send, mock_sensor, mock_out):
        exception = ''

        def send(data):
            class r_v():
                raw_value = r_value
                at_value = a_value

            return r_v

        # if connected, each request returns OK
        mock_echo.return_value = ['OK']
        r_value = ['OK']
        a_value = 'A5'
        send.counter = 0
        mock_send.side_effect = send
        self.scan.initialize()

        self.assertEqual(mock_reset.call_count, 1)
        self.assertEqual(mock_reset.call_args_list[0][0], ())

        self.assertEqual(mock_echo.call_count, 1)
        self.assertEqual(mock_echo.call_args_list[0][0], ())

        self.assertEqual(mock_send.call_count, 6)
        self.assertEqual(mock_sensor.call_args_list[0][0], (mock_send, 0))

        # if not connected
        mock_reset.reset_mock()
        mock_echo.reset_mock()
        mock_send.reset_mock()
        mock_sensor.reset_mock()
        mock_echo.return_value = ['OK']
        r_value = ['OK']
        a_value = 'A5'
        self.scan.sensor.check_pids.return_value = False
        with self.assertRaises(Exception) as cm:
            self.scan.initialize()
        self.assertEqual(cm.exception.__str__(), 'Failed connection to the OBD2 interface!')

        # Exception, check Echo
        mock_reset.reset_mock()
        mock_echo.reset_mock()
        mock_send.reset_mock()
        mock_sensor.reset_mock()

        mock_echo.return_value = ['']
        r_value = ['']
        a_value = 'A5'
        send.counter = 0
        mock_send.side_effect = send
        with self.assertRaises(Exception) as cm:
            self.scan.initialize()
        self.assertEqual(cm.exception.__str__(), 'Echo command did not completed')

        mock_reset.reset_mock()
        mock_echo.reset_mock()
        mock_send.reset_mock()
        mock_sensor.reset_mock()

        mock_echo.return_value = ['OK']
        r_value = ['']
        a_value = 'A5'
        mock_send.side_effect = send

        with self.assertRaises(Exception) as cm:
            self.scan.initialize()
        self.assertEqual(cm.exception.__str__(), "Set protocol command did not completed")

    def test_get_proto_num(self):
        self.scan.obd_protocol = 'AA'
        num = self.scan.get_proto_num()
        self.assertEqual(num, 10)

    @mock.patch('obdlib.scanner.OBDScanner.get_proto_num')
    @mock.patch('obdlib.scanner.OBDScanner.is_port')
    def test_receive(self, mock_is_port, mock_proto_num):
        from obdlib.response import Response

        buffer = 'ATZ\r\x00\n>'

        def read_character(n):
            """
                Emulate UART buffer
            """
            r = buffer[read_character.counter]
            read_character.counter += n
            return r.encode()

        # if connection
        mock_is_port.return_value = True
        mock_proto_num.return_value = 5
        self.scan.uart_port = mock.Mock()

        read_character.counter = 0
        self.scan.uart_port.read.side_effect = read_character
        response = self.scan.receive()
        self.assertIsInstance(response, Response)
        self.assertEqual(self.scan.uart_port.read.call_count, len(buffer))
        self.assertEqual(self.scan.uart_port.read.call_args_list[0][0], (1,))

        # if have not connection
        mock_is_port.reset_mock()
        mock_proto_num.reset_mock()
        mock_is_port.return_value = False
        with self.assertRaises(Exception) as cm:
            self.scan.receive()
        self.assertEqual(cm.exception.__str__(), 'Cannot read when unconnected')

        # if connection but nothing were received
        mock_is_port.reset_mock()
        mock_proto_num.reset_mock()
        mock_is_port.return_value = True
        mock_proto_num.return_value = 5
        self.scan.uart_port = mock.Mock()

        self.scan.uart_port.read.return_value = b''
        response = self.scan.receive()
        self.assertIsInstance(response, Response)
        self.assertEqual(self.scan.uart_port.read.call_count, 11)
        self.assertEqual(self.scan.uart_port.read.call_args_list[0][0], (1,))

    @mock.patch('obdlib.scanner.OBDScanner.send')
    @mock.patch('obdlib.scanner.OBDScanner.is_port')
    def test_reset(self, mock_is_port, mock_send):
        mock_is_port.return_value = True
        self.scan.reset()
        self.assertEqual(mock_is_port.call_count, 1)
        self.assertEqual(mock_is_port.call_args_list[0][0], ())
        self.assertEqual(mock_send.call_count, 1)
        self.assertEqual(mock_send.call_args_list[0][0], ('ATZ', 1))

    @mock.patch('obdlib.scanner.OBDScanner.receive')
    @mock.patch('obdlib.scanner.OBDScanner._write')
    @mock.patch('obdlib.scanner.OBDScanner.is_port')
    @mock.patch('obdlib.scanner.time.sleep')
    @unittest.skip("send")
    def test_send(self, mock_sleep, mock_is_port, mock_write, mock_receive):
        from obdlib.response import Response

        mock_is_port.return_value = True
        mock_receive.return_value = Response()
        resp = self.scan.send('0100')

        self.assertEqual(mock_is_port.call_count, 1)
        self.assertEqual(mock_is_port.call_args_list[0][0], ())

        self.assertEqual(mock_sleep.call_count, 0)

        self.assertEqual(mock_write.call_count, 1)
        self.assertEqual(mock_write.call_args_list[0][0], ('0100',))

        self.assertEqual(mock_receive.call_count, 1)
        self.assertEqual(mock_receive.call_args_list[0][0], ())

        self.assertIsInstance(resp, Response)

        mock_is_port.reset_mock()
        mock_write.reset_mock()
        mock_receive.reset_mock()
        resp = self.scan.send('0100', 1)

        self.assertEqual(mock_is_port.call_count, 1)
        self.assertEqual(mock_is_port.call_args_list[0][0], ())

        self.assertEqual(mock_sleep.call_count, 1)
        self.assertEqual(mock_sleep.call_args_list[0][0], (1,))

        self.assertEqual(mock_write.call_count, 1)
        self.assertEqual(mock_write.call_args_list[0][0], ('0100',))

        self.assertEqual(mock_receive.call_count, 1)
        self.assertEqual(mock_receive.call_args_list[0][0], ())

        self.assertIsInstance(resp, Response)

    def test_vehicle_id_number(self):
        self.scan.sensor = mock.MagicMock()

        class p(object):
            @property
            def gen(self):
                for ecu, value in {'E8': '2312KJLKJHLKJ43L34323'}.items():
                    yield (ecu, value)

        def mode(a):
            def pid(n):
                pid.ecus = p().gen
                return pid

            return pid

        self.scan.sensor.__getitem__.side_effect = mode
        vin = self.scan.vehicle_id_number()
        self.assertEqual(vin, {'E8': '2312KJLKJHLKJ43L34323'})

    @mock.patch('sys.stdout')
    @mock.patch('obdlib.scanner.OBDScanner.send')
    def test_clear_trouble_codes(self, mock_send, mock_out):
        def send(data):
            class r_v():
                raw_value = value

            return r_v

        # Return OK
        value = ['OK']
        mock_send.side_effect = send
        resp = self.scan.clear_trouble_codes()

        self.assertEqual(mock_send.call_count, 1)
        self.assertEqual(mock_send.call_args_list[0][0], ('04',))

        self.assertIsNone(resp)

        # Do not return OK
        mock_send.reset_mock()
        value = ['?']
        mock_send.side_effect = send
        resp = self.scan.clear_trouble_codes()

        self.assertEqual(mock_send.call_count, 1)
        self.assertEqual(mock_send.call_args_list[0][0], ('04',))

        self.assertIsNone(resp)

    @mock.patch('obdlib.scanner.OBDScanner.send')
    def test_echo_off(self, mock_send):
        def send(data):
            class r_v():
                raw_value = value

            return r_v

        value = ['OK']
        mock_send.side_effect = send
        resp = self.scan.echo_off()
        self.assertEqual(mock_send.call_count, 1)
        self.assertEqual(mock_send.call_args_list[0][0], ('ATE0',))
        self.assertEqual(resp, ['OK'])

    def test__check_response(self):
        resp = self.scan._check_response(['OK'])
        self.assertTrue(resp)

        resp = self.scan._check_response(['?'])
        self.assertFalse(resp)

    def test__write(self):
        self.scan.uart_port = mock.Mock()
        self.scan._write('ATH1')

        self.assertEqual(self.scan.uart_port.flushOutput.call_count, 1)
        self.assertEqual(self.scan.uart_port.flushOutput.call_args_list[0][0], ())

        self.assertEqual(self.scan.uart_port.flushInput.call_count, 1)
        self.assertEqual(self.scan.uart_port.flushInput.call_args_list[0][0], ())

        self.assertEqual(self.scan.uart_port.write.call_count, 1)
        self.assertEqual(self.scan.uart_port.write.call_args_list[0][0], (b'ATH1\r\n',))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestOBDScanner)
    unittest.TextTestRunner(verbosity=2).run(suite)

