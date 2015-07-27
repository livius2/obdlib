import unittest
import obdlib.obd.modes as modes


class TestModes(unittest.TestCase):
    def test_init(self):
        m = modes.Modes(1)
        self.assertIsInstance(m.modes, dict)


suite = unittest.TestLoader().loadTestsFromTestCase(TestModes)
unittest.TextTestRunner(verbosity=2).run(suite)
