"""
Order matching objects.
"""
import json


class _Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Singleton(_Singleton('SingletonMeta', (object,), {})):
    pass


class Book(Singleton):
    """
    Yikes, a singleton! Seems to fit this design though. Implements the order
    book and matching engine.
    """

    def __init__(self):
        self.buys = []
        self.sells = []

    def _ismatch(self, order, entry):
        """
        Conditional boolean value depending on which side of order book.
        """
        if isinstance(order, Buy):
            return order >= entry
        if isinstance(order, Sell):
            return order <= entry

    def _post(self, order, entry):
        """
        Logic is reverse of _ismatch(). Avoid dupicating code, reverse args.
        """
        return self._ismatch(entry, order)

    def match(self, order):
        """
        Match the order and post unfilled to book.
        """
        side = None
        if isinstance(order, Buy):
            side = self.sells
        if isinstance(order, Sell):
            side = self.buys

        fills = []
        index = 0
        for entry in [x for x in side]:
            if self._ismatch(order, entry):
                try:
                    remainder = entry - order
                    # order.qty = entry.qty : order complete fill. remove
                    # entry. stop.
                    if order.qty == entry.qty:
                        fills.append(order.dict())
                        del side[index]
                        break
                    # order.qty < entry.qty : order complete fill. update
                    # entry qty. zero order qty.
                    if remainder['qty'] > 0:
                        #entry.qty = entry.qty - order.qty
                        entry.update(**remainder)
                        fills.append(order.dict())
                        order.complete()
                except:
                    # order.qty > entry.qty : order partial fill. remove entry.
                    # update order. continue.

                    # No danger of exception on next line since the exception
                    # that landed us here has demonstrated that order - entry
                    # is safe.
                    order.update(**(order - entry))
                    fills.append(entry.dict())
                    del side[index]
            else:
                # Don't look at every entry if we've exhausted the price
                # limited possibilities.
                break

        if order.qty > 0:
            self.post(order)
        return fills

    def post(self, order):
        side = None
        if isinstance(order, Buy):
            side = self.buys
        if isinstance(order, Sell):
            side = self.sells

        index = 0
        for entry in side:
            if self._post(order, entry):
                index += 1
                continue
            else:
                break

        side.insert(index, order)

    def orders(self):
        return {
            "buys": [buy.dict() for buy in self.buys],
            "sells": [sell.dict() for sell in self.sells],
        }


class Order(object):
    """
    Base class for order objects.
    """

    def __init__(self, qty=0, prc=0):
        self.qty = qty
        self.prc = prc

    def __sub__(self, other):
        if self.qty >= other.qty:
            ret = {"qty": self.qty - other.qty, "prc": self.prc}
            return ret
        else:
            raise Exception("Short of shares to fill.")

    def __ge__(self, other):
        return self.prc >= other.prc

    def __str__(self):
        ret = {"qty": self.qty, "prc": self.prc}
        return json.dumps(ret)

    def __unicode__(self):
        return str(self)

    def __repr__(self):
        return str(self)

    def dict(self):
        return {"prc": self.prc, "qty": self.qty}

    def complete(self):
        self.qty = 0

    def update(self, **remainder):
        self.qty = remainder['qty']


class Buy(Order):
    pass


class Sell(Order):
    pass

