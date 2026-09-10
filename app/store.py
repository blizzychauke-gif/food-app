"""Simple in-memory data store used by the mock/demo application."""

DB = {
    "restaurants": [], "categories": [], "foods": [], "customers": [],
    "drivers": [], "addresses": [], "promotions": [], "reviews": [],
    "orders": [], "notifications": [],
}

def get_by_id(collection: str, item_id: str):
    for item in DB.get(collection, []):
        if item.get("id") == item_id:
            return item
    return None

def find_orders_by_payment(payment_id: str):
    for order in DB.get("orders", []):
        if order.get("payment_id") == payment_id:
            return order
    return None
