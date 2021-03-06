# pylint: disable=C0111,C0103,C0112,W0201,W0212
import unittest

from datetime import date
from market import Singleton
from algorithm_manager import AlgorithmManager as QCAlgorithm


def assert_log_level_error(test):
    test.assertEqual(Singleton._can_log(Singleton.ERROR), True)
    test.assertEqual(Singleton._can_log(Singleton.LOG), False)
    test.assertEqual(Singleton._can_log(Singleton.DEBUG), False)

def assert_log_level_log(test):
    test.assertEqual(Singleton._can_log(Singleton.ERROR), True)
    test.assertEqual(Singleton._can_log(Singleton.LOG), True)
    test.assertEqual(Singleton._can_log(Singleton.DEBUG), False)

def assert_log_level_debug(test):
    test.assertEqual(Singleton._can_log(Singleton.ERROR), True)
    test.assertEqual(Singleton._can_log(Singleton.LOG), True)
    test.assertEqual(Singleton._can_log(Singleton.DEBUG), True)


class TestSingletonLogLevel(unittest.TestCase):
    def setUp(self):
        self.qc = QCAlgorithm()
        Singleton.Setup(self.qc, log_level=Singleton.LOG)

    def test_log_level_printable_error(self):
        Singleton.LogLevel = Singleton.ERROR
        assert_log_level_error(self)

    def test_log_level_printable_log(self):
        Singleton.LogLevel = Singleton.LOG
        assert_log_level_log(self)

    def test_log_level_printable_debug(self):
        Singleton.LogLevel = Singleton.DEBUG
        assert_log_level_debug(self)


class TestSingletonLogLevelWithCustomDateRanges(unittest.TestCase):
    def setUp(self):
        self.qc = QCAlgorithm()
        Singleton.Setup(self.qc, log_level=Singleton.LOG)

    @classmethod
    def setUpClass(cls):
        Singleton.SetStartDateLogLevel(Singleton.LOG, 2005, 5, 1)
        Singleton.SetStartDateLogLevel(Singleton.ERROR, 2006, 11, 3)
        Singleton.SetStartDateLogLevel(Singleton.LOG, 2007, 5, 1)
        Singleton.SetStartDateLogLevel(Singleton.DEBUG, 2008, 10, 31)

    def test_dates_setup(self):
        assert_log_level_log(self)

    def test_dates_simple(self):
        Singleton.Today = date(2004, 10, 25)
        assert_log_level_log(self)

        Singleton.Today = date(2005, 10, 25)
        assert_log_level_log(self)

        Singleton.Today = date(2005, 11, 25)
        assert_log_level_log(self)

        Singleton.Today = date(2006, 11, 4)
        assert_log_level_error(self)

        Singleton.Today = date(2007, 11, 1)
        assert_log_level_log(self)

        Singleton.Today = date(2018, 11, 1)
        assert_log_level_debug(self)

    def test_dates_limit(self):
        Singleton.Today = date(2007, 4, 30)
        assert_log_level_error(self)
        Singleton.Today = date(2007, 5, 1)
        assert_log_level_log(self)

        Singleton.Today = date(2006, 11, 2)
        assert_log_level_log(self)
        Singleton.Today = date(2006, 11, 3)
        assert_log_level_error(self)


if __name__ == '__main__':
    unittest.main()
