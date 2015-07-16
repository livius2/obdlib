import unittest
import sys
from obdlib.logging import Logging

if sys.version_info[0] < 3:
    import mock
else:
    import unittest.mock as mock


class TestLogging(unittest.TestCase):
    def setUp(self):
        self.logger = Logging(duplicate_in_stdout=True)

    def test___logtime(self):
        time = (2014, 1, 1, 0, 16, 41, 2, 1)
        self.assertEqual('2014-01-01 00:16:41',
                         self.logger._Logging__logtime(time))
        time = (2014, 12, 30, 24, 59, 59, 2, 1)
        self.assertEqual('2014-12-30 24:59:59',
                         self.logger._Logging__logtime(time))

    def test_get_log_level(self):
        response = self.logger.get_log_level(0)
        self.assertEqual(response, 'CRITICAL')

        response = self.logger.get_log_level(6)
        self.assertEqual(response, 'NOTSET')

    def test_critical(self):
        response = self.logger.critical('Critical')
        self.assertIsNone(response)

    def test_error(self):
        response = self.logger.error('Error')
        self.assertIsNone(response)

    def test_warning(self):
        response = self.logger.warning('Warning')
        self.assertIsNone(response)

    def test_info(self):
        response = self.logger.info('Info')
        self.assertIsNone(response)

    def test_debug(self):
        response = self.logger.debug('Debug')
        self.assertIsNone(response)

    def test_log(self):
        response = self.logger.log('Log')
        self.assertIsNone(response)