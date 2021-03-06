import unittest
import sys

if sys.version_info[0] < 3:
    import mock
else:
    import unittest.mock as mock
import obdlib.obd.protocols.protocols as p


class TestProtocols(unittest.TestCase):
    def setUp(self):
        self.p = p.Protocols()

    def test_get_frame_params(self):
        params = self.p._get_frame_params('86F1104100FFFFFFFFFC')
        self.assertIsInstance(params, tuple)
        self.assertEqual(params[0], '10')  # ECU
        self.assertEqual(params[1], 41)  # Mode

    def test_get_multi_data(self):
        data = self.p._get_multi_data('86F11049020244344750FC')
        self.assertEqual(data, '44344750')

    def test_add_additional_byte(self):
        data = self.p._add_additional_byte('86F11043013300000000')
        self.assertEqual(data, '86F1104300013300000000')

    def test_get_data(self):
        data = self.p.get_data('86F1104100FFFFFFFFFC')
        self.assertEqual(data, 'FFFFFFFF')

        with self.assertRaises(Exception) as cm:
            self.p.get_data('4100F')
        self.assertEqual(cm.exception.__str__(), 'The frame size is not suitable.')

    def test__parse_headers(self):
        response = [
            '86F11049020100000031FC',
            '86F11149020244344750FC',
        ]
        data = self.p._parse_headers(response)
        self.assertEqual(data, {
            '10': 1,
            '11': 1
        })

    @mock.patch('sys.stdout')
    def test_create_data(self, mock_out):
        # NO DATA
        response = ['NODATA']
        data = self.p.create_data(response)
        self.assertEqual(len(data), 0)

        # If error 7F...
        response = ['7F0112']
        data = self.p.create_data(response)
        self.assertEqual(len(data), 0)

        # If raw_data
        #
        # Single line
        response = [
            '86F1104100FFFFFFFFFC'
        ]
        data = self.p.create_data(response)
        self.assertEqual(data, {'10': 'FFFFFFFF'})

        # Multi line and one ECU response
        response = [
            '86F11049020100000031FC',
            '86F11049020244344750FC',
            '86F11049020330305235FC',
            '86F11049020533343536FC',
            '86F11049020435423132FC'
        ]
        data = self.p.create_data(response)
        self.assertEqual(data, {'10': '0000003144344750303052353542313233343536'})

        # two ECU's responses
        response = [
            '86F1104100FFFFFFFFFC',
            '86F1124100FFFFF56FFC'
        ]
        data = self.p.create_data(response)
        self.assertEqual(data, {
            '10': 'FFFFFFFF',
            '12': 'FFFFF56F'
        })


suite = unittest.TestLoader().loadTestsFromTestCase(TestProtocols)
unittest.TextTestRunner(verbosity=2).run(suite)
