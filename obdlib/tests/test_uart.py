import unittest
import unittest.mock as mock
import uart
import serial


class TestUART(unittest.TestCase):
    def setUp(self):
        serial.Serial = mock.Mock()
        self.tUART = uart.UART()

    @mock.patch('sys.stdout')
    @mock.patch('uart.UART._mapping')
    @mock.patch('uart.uart_base')
    def test_connection(self, mock_ubase, mock_map, mock_out):
        resp = self.tUART.connection('/dev/null')
        self.assertEqual(mock_ubase.call_count, 1)
        self.assertEqual(mock_ubase.call_args_list[0][0], ('/dev/null', 38400))
        self.assertEqual(mock_map.call_count, 1)
        self.assertEqual(mock_map.call_args_list[0][0], ())
        self.assertIsInstance(resp, uart.UART)

        # Raise Exception
        mock_ubase.reset_mock()
        mock_map.reset_mock()
        mock_ubase.side_effect = Exception("Error connection")
        resp = self.tUART.connection('/dev/null')
        self.assertEqual(mock_ubase.call_count, 1)
        self.assertEqual(mock_ubase.call_args_list[0][0], ('/dev/null', 38400))
        self.assertEqual(mock_map.call_count, 0)
        self.assertIsNone(resp)

    def test__getattr__(self):
        with self.assertRaises(Exception) as cm:
            self.tUART.init()
        self.assertEqual(cm.exception.__str__(), 'Unregistered method or attribute init')

        # check method
        raised = False
        try:
            self.tUART.bus = mock.Mock()
            self.tUART.read()
        except:
            raised = True
        self.assertFalse(raised)

    def test_invoke_mapping(self):
        self.tUART.bus = mock.Mock()
        self.tUART.bus_name = 'UART'
        self.tUART._mapping()
        self.tUART._invoke_mapping('close')

        method = 'init'
        with self.assertRaises(Exception) as cm:
            self.tUART._invoke_mapping(method)
        self.assertEqual(cm.exception.__str__(), 'Unregistered method or attribute {}'.format(method))

    def test__mapping(self):
        expected = {
            "UART": {
                "close": "deinit",
                "flushInput": "",
                "flushOutput": ""
            }
        }
        self.tUART._mapping()
        self.assertIsInstance(self.tUART.map, dict)
        self.assertEqual(self.tUART.map, expected)

suite = unittest.TestLoader().loadTestsFromTestCase(TestUART)
unittest.TextTestRunner(verbosity=2).run(suite)
