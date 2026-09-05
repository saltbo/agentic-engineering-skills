import unittest
from api import handle
class ApiTests(unittest.TestCase):
    def test_list(self):
        status, body = handle("GET", "/v1/orders")
        self.assertEqual(status, 200)
        self.assertEqual(body["data"][0]["id"], "o1")

    def test_read_order(self):
        self.assertEqual(
            handle("GET", "/v1/orders/o1"),
            (200, {"data": {"id": "o1", "status": "pending"}}),
        )

    def test_read_missing_order(self):
        self.assertEqual(
            handle("GET", "/v1/orders/missing"),
            (404, {"error": {"code": "NOT_FOUND"}}),
        )

    def test_unmatched_routes_keep_existing_error(self):
        for method, path in [
            ("POST", "/v1/orders/o1"),
            ("GET", "/orders/o1"),
            ("GET", "/v1/orders/"),
            ("GET", "/v1/orders/o1/items"),
        ]:
            with self.subTest(method=method, path=path):
                self.assertEqual(
                    handle(method, path),
                    (404, {"error": {"code": "NOT_FOUND"}}),
                )
