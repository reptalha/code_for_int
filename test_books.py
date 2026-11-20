
def remaining(book, side):
    data = book.bids if side == "BUY" else book.asks
    orders = []

    # V1: Priority queue
    if isinstance(data, list):
        for price, sequence, order in data:
            orders.append((order.id, order.price, order.quantity))

    # V2: Sorted price levels
    else:
        for level in data.values():
            for order in level.values():
                orders.append((order.id, order.price, order.quantity))

    return sorted(orders)


def check(name, actual, expected):
    if actual == expected:
        print("PASS:", name)
    else:
        print("FAIL:", name)
        print("Expected:", expected)
        print("Got:", actual)
        raise SystemExit(1)


def run_tests(OrderBook):

    # Test 1: FIFO matching and partial fills
    book = OrderBook()
    book.place("S1", "SELL", 10000, 10)
    book.place("S2", "SELL", 10000, 5)
    book.place("B1", "BUY", 10100, 12)

    check("FIFO and partial fills",
          remaining(book, "SELL"),
          [("S2", 10000, 3)])

    # Test 2: Cancellation
    book.place("B2", "BUY", 9900, 4)
    cancelled = book.cancel("B2")

    check("Cancellation",
          (cancelled, remaining(book, "BUY")),
          (True, []))

    # Test 3: Price priority
    book = OrderBook()
    book.place("S1", "SELL", 10100, 5)
    book.place("S2", "SELL", 10000, 5)
    book.place("B1", "BUY", 10100, 3)

    check("Price priority",
          remaining(book, "SELL"),
          [("S1", 10100, 5), ("S2", 10000, 2)])

    # Test 4: Partial unmatched order
    book = OrderBook()
    book.place("S1", "SELL", 10000, 2)
    book.place("B1", "BUY", 10100, 5)

    check("Remaining quantity",
          remaining(book, "BUY"),
          [("B1", 10100, 3)])

    # Test 5: Prices don't cross
    book = OrderBook()
    book.place("S1", "SELL", 10100, 2)
    book.place("B1", "BUY", 10000, 3)

    check("Non-crossing prices",
          (remaining(book, "BUY"), remaining(book, "SELL")),
          ([("B1", 10000, 3)], [("S1", 10100, 2)]))

    print("\nAll 5 tests passed!")
