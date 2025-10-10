class OrderNotFoundError(Exception):
    def __init__(self, order_id: int):
        self.order_id = order_id
