import unittest
import sys

if sys.version_info[0] < 3:
    mock_o = '__builtin__.open'
    import mock
else:
    mock_o = 'builtins.open'
    import unittest.mock as mock

from obdlib.obd.pids import Pids


class TestPids(unittest.TestCase):
    def setUp(self):
        self.pids = Pids()

    def test_set_mode(self):
        response = self.pids.set_mode(1)
        self.assertEqual(self.pids.mode, 1)
        self.assertIsInstance(response, Pids)

    @mock.patch(mock_o)
    def test_getitem(self, mock_open):
        file = mock.MagicMock(return_value=None)
        file.__enter__.return_value = file
        file.__iter__.return_value = (x for x in ('("a",)', '("b",)'))

        mock_open.return_value = file

        mode = 1
        self.pids.set_mode(mode)
        response = self.pids[0]
        mock_open.assert_called_once_with('obdlib/obd/commands/pids.{}'.format(mode))

        self.assertIsInstance(response, tuple)
        self.assertEqual(response, ('a',))


suite = unittest.TestLoader().loadTestsFromTestCase(TestPids)
unittest.TextTestRunner(verbosity=2).run(suite)
