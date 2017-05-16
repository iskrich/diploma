from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.stratanalyzer.returns import Returns
from pyalgotrade.stratanalyzer import sharpe
from pyalgotrade.stratanalyzer import drawdown
from pyalgotrade.stratanalyzer import trades

class SharpeStatistics():
    def __init__(self, myStrategy):
        self.myStrategy = myStrategy
        self.tradesAnalyzer = trades.Trades()
        self.myStrategy.attachAnalyzer(self.tradesAnalyzer)

        self.sharpeAnalyzer = sharpe.SharpeRatio()
        self.retAnalyzer = Returns()
        self.myStrategy.attachAnalyzer(self.retAnalyzer)
        self.myStrategy.attachAnalyzer(self.sharpeAnalyzer)
        self.myStrategy.run()
        self.myStrategy.getResult()
        self.retAnalyzer.getCumulativeReturns()
        self.result = self.sharpeAnalyzer.getSharpeRatio(0.025)
        tr = self.tradesAnalyzer.getAllReturns()
        self.streak = 0
        temp_streak = 0
        for i in tr:
            if i > 0:
                temp_streak = temp_streak + 1
            else:
                self.streak = temp_streak if temp_streak > self.streak else self.streak

class Statistics():
    def __init__(self, myStrategy):
        self.myStrategy  = myStrategy
        self.retAnalyzer = Returns()
        self.myStrategy.attachAnalyzer(self.retAnalyzer)
        self.sharpeRatioAnalyzer = sharpe.SharpeRatio()
        self.myStrategy.attachAnalyzer(self.sharpeRatioAnalyzer)
        self.drawDownAnalyzer = drawdown.DrawDown()
        self.myStrategy.attachAnalyzer(self.drawDownAnalyzer)
        self.tradesAnalyzer = trades.Trades()
        self.myStrategy.attachAnalyzer(self.tradesAnalyzer)
        self.myStrategy.run()
        tr = self.tradesAnalyzer.getAllReturns()
        self.streak = 0
        temp_streak = 0
        for i in tr:
            if i > 0:
                temp_streak = temp_streak + 1
            else:
                self.streak = temp_streak if temp_streak > self.streak else self.streak
                temp_streak = 0
        if (temp_streak != 0 and temp_streak > self.streak):
            self.streak = temp_streak
        i = 0
    def Sharpe(self):
        return  self.sharpeRatioAnalyzer.getSharpeRatio(0.025)

    def printResults(self):
        print "Final portfolio value: $%.2f" % self.myStrategy.getResult()
        print "Cumulative returns: %.2f %%" % (self.retAnalyzer.getCumulativeReturns()[-1] * 100)
        print "Sharpe ratio: %.2f" % (self.sharpeRatioAnalyzer.getSharpeRatio(0.05))
        print "Max. drawdown: %.2f %%" % (self.drawDownAnalyzer.getMaxDrawDown() * 100)
        print "Longest drawdown duration: %s" % (self.drawDownAnalyzer.getLongestDrawDownDuration())

        print
        print "Total trades: %d" % (self.tradesAnalyzer.getCount())
        if self.tradesAnalyzer.getCount() > 0:
            profits = self.tradesAnalyzer.getAll()
            print "Avg. profit: $%2.f" % (profits.mean())
            print "Profits std. dev.: $%2.f" % (profits.std())
            print "Max. profit: $%2.f" % (profits.max())
            print "Min. profit: $%2.f" % (profits.min())
            returns = self.tradesAnalyzer.getAllReturns()
            print "Avg. return: %2.f %%" % (returns.mean() * 100)
            print "Returns std. dev.: %2.f %%" % (returns.std() * 100)
            print "Max. return: %2.f %%" % (returns.max() * 100)
            print "Min. return: %2.f %%" % (returns.min() * 100)

        print
        print "Profitable trades: %d" % (self.tradesAnalyzer.getProfitableCount())
        if self.tradesAnalyzer.getProfitableCount() > 0:
            profits = self.tradesAnalyzer.getProfits()
            print "Avg. profit: $%2.f" % (profits.mean())
            print "Profits std. dev.: $%2.f" % (profits.std())
            print "Max. profit: $%2.f" % (profits.max())
            print "Min. profit: $%2.f" % (profits.min())
            returns = self.tradesAnalyzer.getPositiveReturns()
            print "Avg. return: %2.f %%" % (returns.mean() * 100)
            print "Returns std. dev.: %2.f %%" % (returns.std() * 100)
            print "Max. return: %2.f %%" % (returns.max() * 100)
            print "Min. return: %2.f %%" % (returns.min() * 100)

        print
        print "Unprofitable trades: %d" % (self.tradesAnalyzer.getUnprofitableCount())
        if self.tradesAnalyzer.getUnprofitableCount() > 0:
            losses = self.tradesAnalyzer.getLosses()
            print "Avg. loss: $%2.f" % (losses.mean())
            print "Losses std. dev.: $%2.f" % (losses.std())
            print "Max. loss: $%2.f" % (losses.min())
            print "Min. loss: $%2.f" % (losses.max())
            returns = self.tradesAnalyzer.getNegativeReturns()
            print "Avg. return: %2.f %%" % (returns.mean() * 100)
            print "Returns std. dev.: %2.f %%" % (returns.std() * 100)
            print "Max. return: %2.f %%" % (returns.max() * 100)
            print "Min. return: %2.f %%" % (returns.min() * 100)