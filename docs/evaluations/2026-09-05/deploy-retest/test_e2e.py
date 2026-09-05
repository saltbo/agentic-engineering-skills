import json
import os
import subprocess
import sys
import unittest

TARGET = os.environ.get('E2E_TARGET', 'local')
if TARGET not in ('local', 'deployed'):
    raise ValueError('E2E_TARGET must be local or deployed')
EXPECTED_VERSION = os.environ['E2E_EXPECTED_VERSION'] if TARGET == 'deployed' else 'r2'


def get(path):
    return json.loads(subprocess.check_output(
        [sys.executable, 'release.py', 'get', TARGET, path], timeout=10))


class OrderJourney(unittest.TestCase):
    """Read-only release checks; explicitly selected for deployed verification."""

    @classmethod
    def setUpClass(cls):
        if TARGET == 'local':
            subprocess.run([sys.executable, 'release.py', 'reset-local'],
                           check=True, timeout=10)
        observed = get('/version')['version']
        if observed != EXPECTED_VERSION:
            raise AssertionError(f'Expected {EXPECTED_VERSION}, observed {observed}')

    def test_read_order_total(self):
        order = get('/orders/o1')
        self.assertEqual(order['totalCents'], 1200)
        self.assertEqual(order['id'], 'o1')
        self.assertEqual(order['status'], 'pending')

    def test_health(self):
        self.assertEqual(get('/health')['status'], 'ok')
