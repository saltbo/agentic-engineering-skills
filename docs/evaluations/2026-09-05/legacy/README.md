Existing supported API. All routes use /v1 and successful JSON uses a data envelope. No external dependencies. Local checks: python3 -B -m unittest discover -v. Add tests as needed.

`GET /v1/orders/{orderId}` returns `200` with `{"data": {"id": "o1", "status": "pending"}}` for an existing order. An absent order returns `404` with `{"error": {"code": "NOT_FOUND"}}`.
