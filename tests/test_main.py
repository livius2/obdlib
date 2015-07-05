import unittest
import unittest.mock as mock
from obd.protocols.base import Base


class TestMain(unittest.TestCase):
    def setUp(self):
        self.pm = Base()

    def test_remove_searching(self):
        data = self.pm.remove_searching(['SEARCHING...'])
        self.assertEqual(data, [])

        data = self.pm.remove_searching(['SEARCHING...', '410000000000'])
        self.assertEqual(data, ['410000000000'])

        # Exception - ValueError
        data = self.pm.remove_searching(['410C34'])
        self.assertEqual(data, ['410C34'])

    def test_create_data(self):
        with self.assertRaises(NotImplementedError) as cm:
            self.pm.create_data([])
        self.assertIsInstance(cm.exception, NotImplementedError)

    def test_check_result(self):
        resp = self.pm.check_result(['NODATA'])
        self.assertFalse(resp)

        resp = self.pm.check_result(['410C7D'])
        self.assertTrue(resp)

    @mock.patch('sys.stdout')
    def test_check_error(self, mock_out):
        # if hasn't error
        resp = self.pm.check_error(['410C7D'])
        self.assertTrue(resp)

        # if some error appears
        resp = self.pm.check_error(['7F0112'])
        self.assertFalse(resp)

        resp = self.pm.check_error(['7F0188'])
        self.assertFalse(resp)


suite = unittest.TestLoader().loadTestsFromTestCase(TestMain)
unittest.TextTestRunner(verbosity=2).run(suite)
