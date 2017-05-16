from pyalgotrade import strategy
from pyalgotrade import plotter
from pyalgotrade.tools import yahoofinance

class HoldAndBuy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument
        self.current_bar = 0
        self._position = None
        self.getBroker().getFillStrategy().setVolumeLimit(None)

    def onEnterCanceled(self, position):
        if (self._position is not None):
            self.__position.exitMarket()
        self.__position = None

    def getInstrument(self):
        return self.__instrument

    def onExitOk(self, position):
        if (self._position is not None):
            self.__position.exitMarket()
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        if (self._position is not None):
            self.__position.exitMarket()
        self.__position.exit()

    def onBars(self, bars):
        if self.current_bar == 0:
            shares = int(self.getBroker().getCash() * 0.9 / bars[self.__instrument].getPrice())
            self.__position = self.enterLong(self.__instrument, shares, True)

        self.current_bar+=1
        if self.current_bar == 250:
            self.__position.exitMarket()



class Test(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, trades):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument
        self.trades = trades
        self.current_bar = 0
        self._position = None
        self.prevOrder = "Short"
        self.getBroker().getFillStrategy().setVolumeLimit(None)

    def onEnterCanceled(self, position):
        self.__position = None

    def getInstrument(self):
        return self.__instrument

    def onExitOk(self, position):
        if (self._position is not None):
            self.__position.exitMarket()
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        if (self._position is not None):
            self.__position.exitMarket()
        self.__position.exit()

    def onBars(self, bars):
        if len(self.trades) <= self.current_bar:
            return

        if self.trades[self.current_bar] == 1 and self.prevOrder == "Short":
            shares = int(self.getBroker().getCash() * 0.8 / bars[self.__instrument].getPrice())
            i = 0
            self.__position = self.enterLong(self.__instrument, shares, True)
            self.prevOrder = "Long"

        elif self.trades[self.current_bar] == -1 and self.prevOrder == "Long":
            self.__position.exitMarket()
            self.prevOrder = "Short"

        self.current_bar+=1

