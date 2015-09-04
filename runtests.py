#!/usr/bin/env python
import unittest

from tests import test_m2m


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(test_m2m.suite())

    return test_suite

runner = unittest.TextTestRunner()
runner.run(suite())
