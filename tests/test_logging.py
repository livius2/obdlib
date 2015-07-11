from unittest import TestCase
from obdlib.logging import Logging

class TestLogging(TestCase):
    def test___logtime(self):
        logger = Logging()
        time = (2014, 1, 1, 0, 16, 41, 2, 1)
        self.assertEqual('2014-01-01 00:16:41',
                         logger._Logging__logtime(time))
        time = (2014, 12, 30, 24, 59, 59, 2, 1)
        self.assertEqual('2014-12-30 24:59:59',
                         logger._Logging__logtime(time))
