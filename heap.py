
import heapq


class Order:
    def __init__(self, order_id, price, quantity):
        self.id = order_id
        self.price = price
        self.quantity = quantity


class OrderBook:
    def __init__(self):
        self.bids = []       # Max-heap: highest buy price first
        self.asks = []       # Min-heap: lowest sell price first
        self.sequence = 0    # Arrival order for FIFO


    def place(self, order_id, side, price, quantity):
        order = Order(order_id, price, quantity)

        if side == "BUY":
            own = self.bids
            opposite = self.asks
        else:
            own = self.asks
            opposite = self.bids

        # Keep matching while prices cross
        while order.quantity > 0 and opposite:
            resting = opposite[0][2]

            if side == "BUY" and price < resting.price:
                break
            if side == "SELL" and price > resting.price:
                break

            # Execute trade
            filled = min(order.quantity, resting.quantity)

            order.quantity -= filled
            resting.quantity -= filled

            print(f"TRADE: {filled} shares at £{resting.price / 100:.2f}")

            # Remove resting order if completely filled
            if resting.quantity == 0:
                heapq.heappop(opposite)

        # Add any unmatched quantity to our own heap
        if order.quantity > 0:
            heap_price = -price if side == "BUY" else price
            heapq.heappush(own, (heap_price, self.sequence, order))

        self.sequence += 1


    def cancel(self, order_id):
        for heap in (self.bids, self.asks):
            for i, (_, _, order) in enumerate(heap):
                if order.id == order_id:
                    heap.pop(i)
                    heapq.heapify(heap)
                    return True

        return False


if __name__ == "__main__":
    from test_books import run_tests

    print("Testing V1: Priority Queue")
    run_tests(OrderBook)
