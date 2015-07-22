import unittest
import sys

if sys.version_info[0] < 3:
    import mock
else:
    import unittest.mock as mock
import obdlib.obd.protocols.can_protocols as p_can


class TestProtocolsCan(unittest.TestCase):
    def setUp(self):
        self.pc = p_can.ProtocolsCan(6)

    def test___get_bits(self):
        bits = self.pc._ProtocolsCan__get_bits(6)
        self.assertEqual(bits, 11)

    def test___digit(self):
        digit = self.pc._ProtocolsCan__digit('A')
        self.assertEqual(digit, 10)

    def test___last_bytes(self):
        expected = 12
        self.pc.frame_start = 4
        last = self.pc._ProtocolsCan__last_bytes(4)
        self.assertEqual(last, expected)

    def test___align_frame(self):
        frame = self.pc._ProtocolsCan__align_frame(['7E8064100FFFFFFFFFC'])
        self.assertIn('000007E8064100FFFFFFFFFC', frame)

    def test___get_single_data(self):
        data = self.pc._ProtocolsCan__get_single_data('000007E8064100FFFFFFFFFC')
        self.assertEqual(data, 'FFFFFFFF')

    def test___get_frame_params(self):
        params = self.pc._ProtocolsCan__get_frame_params('000007E8064100FFFFFFFFFC')
        self.assertIsInstance(params, tuple)
        self.assertEqual(params[0], 'E8')  # ECU
        self.assertEqual(params[1], 0)  # Frame type
        self.assertEqual(params[2], 41)  # Mode

    @mock.patch('sys.stdout')
    def test_create_data(self, mock_out):
        # NO DATA
        response = ['NODATA']
        data = self.pc.create_data(response)
        self.assertEqual(len(data), 0)

        # If error 7F...
        response = ['7F0112']
        data = self.pc.create_data(response)
        self.assertEqual(len(data), 0)

        # If raw_data
        #
        # Single frame 11 bits
        response = [
            '7E8064100FFFFFFFFFC'
        ]
        data = self.pc.create_data(response)
        self.assertEqual(data, {'E8': 'FFFFFFFF'})

        # Single frame 29 bits
        response = [
            '18DAF110064100FFFFFFFFFC'
        ]
        pc = p_can.ProtocolsCan(7)
        data = pc.create_data(response)
        self.assertEqual(data, {'10': 'FFFFFFFF'})

        # Multi line frame 11 bits
        response = [
            '7E81013490401353630',
            '7E82200000000000031',
            '7E82132383934394143'
        ]
        data = self.pc.create_data(response)
        self.assertEqual(data, {'E8': '134904013536303238393439414300000000000031'})

        # Multi line frame 29 bits
        pc = p_can.ProtocolsCan(7)
        response = [
            '18DAF1101013490401353630',
            '18DAF1102200000000000031',
            '18DAF1102132383934394143'
        ]
        data = pc.create_data(response)
        self.assertEqual(data, {'10': '134904013536303238393439414300000000000031'})

        # Single frame 11 bits BUT 2 ECU's
        response = [
            '7E8064100FFFFFFFFFC',
            '7E9064100FFFFFF00FC'
        ]
        data = self.pc.create_data(response)
        self.assertEqual(data, {
            'E8': 'FFFFFFFF',
            'E9': 'FFFFFF00'
        })


suite = unittest.TestLoader().loadTestsFromTestCase(TestProtocolsCan)
unittest.TextTestRunner(verbosity=2).run(suite)
