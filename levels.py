


from collections import OrderedDict
from sortedcontainers import SortedDict


class Order:
    def __init__(self, order_id, price, quantity):
        self.id = order_id
        self.price = price
        self.quantity = quantity


class OrderBook:
    def __init__(self):
        self.bids = SortedDict()  # price -> FIFO orders
        self.asks = SortedDict()  # price -> FIFO orders
        self.active = {}         # order_id -> (side, price)

    def place(self, order_id, side, price, quantity):
        incoming = Order(order_id, price, quantity)

        own = self.bids if side == "BUY" else self.asks
        opposite = self.asks if side == "BUY" else self.bids

        # Keep matching while prices cross
        while incoming.quantity > 0 and opposite:

            # Best ask = lowest price; best bid = highest price
            best_price = opposite.peekitem(
                0 if side == "BUY" else -1
            )[0]

            if side == "BUY" and price < best_price:
                break
            if side == "SELL" and price > best_price:
                break

            level = opposite[best_price]

            # Match oldest orders at this price first
            while incoming.quantity > 0 and level:
                resting_id, resting = next(iter(level.items()))

                filled = min(incoming.quantity, resting.quantity)

                incoming.quantity -= filled
                resting.quantity -= filled

                print(f"TRADE: {filled} shares at £{best_price / 100:.2f}")

                if resting.quantity == 0:
                    del level[resting_id]
                    del self.active[resting_id]

            # Remove price level if no orders remain
            if not level:
                del opposite[best_price]

        # Store unmatched quantity
        if incoming.quantity > 0:
            if price not in own:
                own[price] = OrderedDict()

            own[price][order_id] = incoming
            self.active[order_id] = (side, price)

    def cancel(self, order_id):
        location = self.active.pop(order_id, None)
        if location is None:
            return False

        side, price = location
        own = self.bids if side == "BUY" else self.asks

        del own[price][order_id]

        if not own[price]:
            del own[price]

        return True



if __name__ == "__main__":
    from test_books import run_tests

    print("Testing V2: Sorted Price Levels")
    run_tests(OrderBook)
  
