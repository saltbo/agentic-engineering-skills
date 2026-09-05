"""Explicit, bounded, anonymous read-only release verification."""
import argparse
import os
import unittest

parser = argparse.ArgumentParser()
parser.add_argument('--target', required=True, choices=['deployed'])
parser.add_argument('--expected-version', required=True)
args = parser.parse_args()
os.environ['E2E_TARGET'] = args.target
os.environ['EXPECTED_VERSION'] = args.expected_version
from test_e2e import OrderJourney

suite = unittest.TestSuite([
    OrderJourney('test_read_order_total'),
    OrderJourney('test_health'),
])
result = unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(0 if result.wasSuccessful() and result.testsRun == 2 else 1)
