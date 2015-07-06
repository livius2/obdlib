import unittest
import sys

if sys.version_info[0] < 3:
    import mock
else:
    import unittest.mock as mock
import obdlib.obd.sensors as sensors


class TestCommand(unittest.TestCase):
    def setUp(self):
        call_obd = mock.Mock()
        sensors.Modes = mock.Mock()
        self.s = sensors.Command(call_obd, 0)

    def test_init(self):
        raised = False
        try:
            self.s.init(())
        except ValueError:
            raised = True
        self.assertTrue(raised)

        raised = False
        try:
            self.s.init((1, 2, 3, 4, 5, 6, 7))
        except ValueError:
            raised = True
        self.assertFalse(raised)
        self.assertEqual(self.s.title, 1)

    def test_ecus(self):
        self.s._Command__ecus = {'E8': '1', 'E9': '2'}
        e = self.s.ecus
        self.assertTrue(hasattr(e, '__iter__'))
        for item in e:
            self.assertIsInstance(item, tuple)
            self.assertEqual(len(item), 2)

    def test_sensors(self):
        self.s._Command__modes.modes = mock.MagicMock()
        self.s.init = mock.MagicMock()
        self.s._Command__call = mock.MagicMock()
        self.s._Command__pids = {
            'E8': {'00': 1, '01': 1},
            'E9': {'00': 1, '01': 0}
        }
        s = self.s.sensors()
        self.assertTrue(hasattr(s, '__iter__'))
        for item in s:
            self.assertIsInstance(item, sensors.Command)

    def test_check_pids(self):
        self.s._Command__modes.modes = mock.MagicMock()
        self.s.init = mock.MagicMock()
        self.s._Command__call = mock.MagicMock()
        resp = self.s.check_pids()

        self.assertIsNone(resp)

        self.s._Command__ecus = {'E8': '1', 'E9': '2'}
        resp = self.s.check_pids()

        self.assertTrue(resp)

    def test_is_pids(self):
        self.s._Command__pids = {
            'E8': {'00': 0, '01': 0},
            'E9': {'00': 0, '01': 0}
        }
        resp = self.s.is_pids()
        self.assertFalse(resp)

        self.s._Command__pids = {
            'E8': {'00': 0, '01': 0},
            'E9': {'00': 0, '01': 1}
        }
        resp = self.s.is_pids()
        self.assertTrue(resp)

    def test__set_value(self):
        # if value is NODATA
        self.s._Command__decoder = mock.Mock()
        resp = self.s._set_value('NODATA')
        self.assertEqual(resp, 'NODATA')
        self.assertEqual(self.s._Command__decoder.call_count, 0)

        # if value is None
        self.s._Command__decoder.reset_mock()
        self.s._Command__decoder = mock.Mock()
        resp = self.s._set_value(None)
        self.assertEqual(self.s._Command__decoder.call_count, 0)
        self.assertEqual(resp, None)

        # if hex value and call without kwargs
        self.s._Command__decoder.reset_mock()
        self.s._Command__decoder = mock.Mock()
        resp = self.s._set_value('1A')
        self.assertEqual(self.s._Command__decoder.call_count, 1)
        self.assertEqual(self.s._Command__decoder.call_args[0], ('1A',))

        # if hex value and call with kwargs
        self.s._Command__decoder.reset_mock()
        self.s._Command__decoder = mock.Mock()
        self.s.kwargs = {'param': 'value'}
        resp = self.s._set_value('1A')
        self.assertEqual(self.s._Command__decoder.call_count, 1)
        self.assertEqual(self.s._Command__decoder.call_args[0], ('1A',))
        self.assertEqual(self.s._Command__decoder.call_args[1], {'param': 'value'})
        self.assertIsInstance(resp, mock.Mock)


suite = unittest.TestLoader().loadTestsFromTestCase(TestCommand)
unittest.TextTestRunner(verbosity=2).run(suite)
