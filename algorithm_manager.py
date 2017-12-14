"""
MD5: 56ecb03f9f7f14c20d612193b2d2c4f2
"""

# pylint: disable=C0321,C0111,W0201,C0413
try: QCAlgorithm
except NameError: from mocked import QCAlgorithm, OrderStatus

class AlgorithmManager(QCAlgorithm):

    def registerBroker(self, broker):
        self._broker = broker

    def registerAlgorithms(self, algorithms):
        self.Debug("registerAlgorithms")
        self._algorithms = algorithms

    def __pre(self):
        pass

    def __post(self):
        self._broker.executeOrders()

    def SetWarmUp(self, period):
        if hasattr(self, 'WarmUp'):
            self.WarmUp = max(self.WarmUp, period)
        else:
            self.WarmUp = period
        super(AlgorithmManager, self).SetWarmUp(period)

    def CoarseSelectionFunction(self, coarse):
        symbols = []
        for alg in self._algorithms:
            symbols.extend(alg.CoarseSelectionFunction(coarse))
        return symbols

    def FineSelectionFunction(self, fine):
        symbols = []
        for alg in self._algorithms:
            symbols.extend(alg.FineSelectionFunction(fine))
        return symbols

    def OnData(self, data):
        self.Debug("OnData")
        self.__pre()
        for alg in self._algorithms:
            alg.OnData(data)
        self.__post()

    def OnDividend(self):
        self.Debug("OnDividend")
        self.__pre()
        for alg in self._algorithms:
            alg.OnDividend()
        self.__post()

    def OnEndOfDay(self):
        # self.Debug("OnEndOfDay")
        self.__pre()
        for alg in self._algorithms:
            alg.OnEndOfDay()
            # self.Debug(str(alg))
        self.__post()

    def OnEndOfAlgorithm(self):
        self.Debug("OnEndOfAlgorithm")
        self.__pre()
        for alg in self._algorithms:
            alg.OnEndOfAlgorithm()
        self.__post()

    def OnSecuritiesChanged(self, changes):
        self.Debug("OnSecuritiesChanged")
        self.__pre()
        for alg in self._algorithms:
            # Only call if there's a relevant stock in alg
            alg.OnSecuritiesChanged(changes)
        self.__post()

    def OnOrderEvent(self, event_order):
        self.Debug("OnOrderEvent")
        ticket = self.Transactions.GetOrderById(event_order.OrderId)

        if event_order.Status == OrderStatus.Submitted:
            self.Debug("SUBMITTED: {0}".format(ticket))

        elif event_order.Status in [OrderStatus.Filled, OrderStatus.PartiallyFilled]:
            order = self._broker.submitted.pop(event_order.OrderId)
            if event_order.Status == OrderStatus.PartiallyFilled:
                self.Debug("PARTIAL FILL: {0}".format(ticket))
            else:
                self.Debug("FILLED: {0} at FILL PRICE: {1}".format(ticket, event_order.FillPrice))
            order.Portfolio.fillOrder(order.Symbol, float(event_order.FillQuantity),
                                      float(event_order.FillPrice))

        else:
            order = self._broker.submitted.pop(event_order.OrderId)
            self.Debug(event_order.ToString())
