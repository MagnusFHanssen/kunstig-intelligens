from car import Car, Strategy
a = Car(100, 10, 10, 20)
b = Car(100, 10, 10, 20)

n = 1000
i = 0

print('Car A: | Car B: | New balance A: | New balance B:')

while i < n:
    bid_a = a.bid()
    bid_b = b.bid()

    if bid_a > bid_b:
        a.win(bid_a)
        b.loss(bid_a)
    elif bid_b > bid_a:
        b.win(bid_b)
        a.loss(bid_b)
    else:
        a.draw()
        b.draw()

    print('%6d | %6d | %10d     | %10d' % (bid_a, bid_b, a.budget, b.budget))
    i += 1
    if min(a.budget, b.budget) <= 0:
        break

print('\n%d rounds took place' % i)
