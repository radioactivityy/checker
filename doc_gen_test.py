import random
from datetime import datetime


ORDER_STATUS = {
    "PENDING": "pending",
    "PROCESSING": "processing",
    "SHIPPED": "shipped",
    "DELIVERED": "delivered",
    "CANCELLED": "cancelled"
}

DISCOUNT_RULES = {
    "SUMMER10": 0.10,
    "VIP20": 0.20,
    "FLASH50": 0.50
}


class Product:
    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock

    def is_available(self, quantity):
        return self.stock >= quantity

    def reduce_stock(self, quantity):
        if not self.is_available(quantity):
            raise ValueError(f"Insufficient stock for {self.name}")
        self.stock -= quantity

    def __repr__(self):
        return f"Product({self.name}, ${self.price}, stock={self.stock})"


class Cart:
    def __init__(self):
        self.items = {}
        self.coupon_code = None

    def add_item(self, product, quantity):
        if not product.is_available(quantity):
            raise ValueError(f"Not enough stock for {product.name}")
        if product.product_id in self.items:
            self.items[product.product_id]["quantity"] += quantity
        else:
            self.items[product.product_id] = {
                "product": product,
                "quantity": quantity
            }

    def remove_item(self, product_id):
        if product_id not in self.items:
            raise KeyError(f"Product {product_id} not in cart")
        del self.items[product_id]

    def apply_coupon(self, code):
        if code not in DISCOUNT_RULES:
            raise ValueError(f"Invalid coupon code: {code}")
        self.coupon_code = code

    def get_subtotal(self):
        total = 0
        for item in self.items.values():
            total += item["product"].price * item["quantity"]
        return round(total, 2)

    def get_discount(self):
        if not self.coupon_code:
            return 0
        return round(self.get_subtotal() * DISCOUNT_RULES[self.coupon_code], 2)

    def get_total(self):
        return round(self.get_subtotal() - self.get_discount(), 2)

    def is_empty(self):
        return len(self.items) == 0


class Order:
    def __init__(self, customer_name, cart):
        self.order_id = f"ORD-{random.randint(10000, 99999)}"
        self.customer_name = customer_name
        self.cart = cart
        self.status = ORDER_STATUS["PENDING"]
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def advance_status(self):
        transitions = {
            ORDER_STATUS["PENDING"]: ORDER_STATUS["PROCESSING"],
            ORDER_STATUS["PROCESSING"]: ORDER_STATUS["SHIPPED"],
            ORDER_STATUS["SHIPPED"]: ORDER_STATUS["DELIVERED"]
        }
        if self.status not in transitions:
            raise ValueError(f"Cannot advance from status: {self.status}")
        self.status = transitions[self.status]
        self.updated_at = datetime.now()

    def cancel(self):
        if self.status in [ORDER_STATUS["SHIPPED"], ORDER_STATUS["DELIVERED"]]:
            raise ValueError("Cannot cancel an order that has been shipped or delivered")
        self.status = ORDER_STATUS["CANCELLED"]
        self.updated_at = datetime.now()

    def summary(self):
        lines = [
            f"Order ID : {self.order_id}",
            f"Customer : {self.customer_name}",
            f"Status   : {self.status}",
            f"Subtotal : ${self.cart.get_subtotal()}",
            f"Discount : -${self.cart.get_discount()}",
            f"Total    : ${self.cart.get_total()}",
            f"Created  : {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
        ]
        return "\n".join(lines)


class OrderProcessor:
    def __init__(self):
        self.orders = {}

    def place_order(self, customer_name, cart):
        if cart.is_empty():
            raise ValueError("Cannot place an order with an empty cart")

        for item in cart.items.values():
            item["product"].reduce_stock(item["quantity"])

        order = Order(customer_name, cart)
        self.orders[order.order_id] = order
        return order

    def get_order(self, order_id):
        if order_id not in self.orders:
            raise KeyError(f"Order {order_id} not found")
        return self.orders[order_id]

    def ship_order(self, order_id):
        order = self.get_order(order_id)
        if order.status == ORDER_STATUS["PENDING"]:
            order.advance_status()
        if order.status == ORDER_STATUS["PROCESSING"]:
            order.advance_status()
        return order

    def cancel_order(self, order_id):
        order = self.get_order(order_id)
        order.cancel()
        for item in order.cart.items.values():
            item["product"].stock += item["quantity"]
        return order

    def get_all_orders(self, status_filter=None):
        if status_filter:
            return [o for o in self.orders.values() if o.status == status_filter]
        return list(self.orders.values())


if __name__ == "__main__":
    laptop = Product("P001", "Laptop", 999.99, 10)
    mouse = Product("P002", "Mouse", 29.99, 50)
    keyboard = Product("P003", "Keyboard", 79.99, 30)

    cart = Cart()
    cart.add_item(laptop, 1)
    cart.add_item(mouse, 2)
    cart.add_item(keyboard, 1)
    cart.apply_coupon("VIP20")

    processor = OrderProcessor()
    order = processor.place_order("Gabby", cart)
    print(order.summary())

    processor.ship_order(order.order_id)
    print(f"\nStatus after shipping: {order.status}")