import unittest
import sys

if sys.version_info[0] < 3:
    import mock
else:
    import unittest.mock as mock
import obdlib.response as response


class TestResponse(unittest.TestCase):
    def setUp(self):
        pass

    @mock.patch('obdlib.obd.protocols.protocols.Protocols')
    @mock.patch('obdlib.obd.protocols.can_protocols.ProtocolsCan')
    def test___init__(self, mock_can_proto, mock_proto):
        # Old protocols
        expected_raw_data = []
        resp = response.Response()
        self.assertEqual(mock_proto.call_count, 1)
        self.assertEqual(mock_proto.call_args_list[0][0], ())
        self.assertEqual(mock_can_proto.call_count, 0)
        self.assertEqual(resp.raw_data, expected_raw_data)

        mock_proto.reset_mock()
        mock_can_proto.reset_mock()
        expected_raw_data = ['ATZ']
        resp = response.Response(b'ATZ\r\n')
        self.assertEqual(mock_proto.call_count, 1)
        self.assertEqual(mock_proto.call_args_list[0][0], ())
        self.assertEqual(mock_can_proto.call_count, 0)
        self.assertEqual(resp.raw_data, expected_raw_data)

        # CAN protocols
        mock_proto.reset_mock()
        mock_can_proto.reset_mock()
        expected_raw_data = []
        resp = response.Response(b'', 6)
        self.assertEqual(mock_proto.call_count, 0)
        self.assertEqual(mock_can_proto.call_count, 1)
        self.assertEqual(mock_can_proto.call_args_list[0][0], (6,))
        self.assertEqual(resp.raw_data, expected_raw_data)

        mock_proto.reset_mock()
        mock_can_proto.reset_mock()
        expected_raw_data = ['ATZ']
        resp = response.Response(b'ATZ\r\n', 6)
        self.assertEqual(mock_proto.call_count, 0)
        self.assertEqual(mock_can_proto.call_count, 1)
        self.assertEqual(mock_can_proto.call_args_list[0][0], (6,))
        self.assertEqual(resp.raw_data, expected_raw_data)

    @unittest.skip("_check_value")
    def test__check_value(self):
        pass

    def test_value(self):
        expected_data = {'E8': 'FFFFFFFF'}
        car_response = b'7E8 06 41 00 FF FF FF FF FC\r\n'
        resp = response.Response(car_response, 6)
        resp.protocol.create_data = mock.Mock()
        resp.protocol.create_data.return_value = expected_data
        value = resp.value
        self.assertEqual(resp.protocol.create_data.call_count, 1)
        self.assertEqual(resp.protocol.create_data.call_args_list[0][0], (['7E8064100FFFFFFFFFC'],))
        self.assertEqual(value, expected_data)

    def test_raw_value(self):
        expected_data = ['7E8064100FFFFFFFFFC']
        car_response = b'7E8 06 41 00 FF FF FF FF FC\r\n'
        resp = response.Response(car_response, 6)
        self.assertEqual(resp.raw_value, expected_data)

        expected_data = None
        car_response = b'?\r\n'
        resp = response.Response(car_response, 6)
        self.assertEqual(resp.raw_value, expected_data)

        expected_data = []
        car_response = b'\r\n'
        resp = response.Response(car_response, 6)
        self.assertEqual(resp.raw_value, expected_data)

    def test_at_value(self):
        expected_data = 'A4'
        car_response = b'A4\r\n'
        resp = response.Response(car_response, 4)
        self.assertEqual(resp.at_value, expected_data)


suite = unittest.TestLoader().loadTestsFromTestCase(TestResponse)
unittest.TextTestRunner(verbosity=2).run(suite)
