import unittest
import sys

if sys.version_info[0] < 3:
    import mock
else:
    import unittest.mock as mock
import obdlib.obd.modes as modes


class TestDictModes(unittest.TestCase):
    @mock.patch('obdlib.obd.modes.DictModes.pids')
    def test_getitem(self, mock_pids):
        d = {
            1: 'a'
        }
        response = modes.DictModes(d)
        response = response[1]
        self.assertEqual(response, 'a')


suite = unittest.TestLoader().loadTestsFromTestCase(TestDictModes)
unittest.TextTestRunner(verbosity=2).run(suite)
