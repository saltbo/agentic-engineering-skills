ORDERS = {"o1": {"id": "o1", "status": "pending"}}

def handle(method, path):
    if method == "GET" and path == "/v1/orders":
        return 200, {"data": list(ORDERS.values())}
    if method == "GET" and path.startswith("/v1/orders/"):
        order_id = path[len("/v1/orders/"):]
        if order_id and "/" not in order_id and order_id in ORDERS:
            return 200, {"data": ORDERS[order_id]}
    return 404, {"error": {"code": "NOT_FOUND"}}
