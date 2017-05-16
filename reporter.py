import pdfkit
import os
# -*- coding: utf-8 -*-
import sys

imgTemplate = '<img src="{source}" width = "650" height="500">'


def generatePDF(stats, test_dates, result_dates):
    reload(sys)
    sys.setdefaultencoding('utf8')

    options = {
        'page-size' : "A4",
        'disable-smart-shrinking' : "",
        'zoom' : 2
    }
    with open('utils/report_template.html', 'r') as myfile:
         html = myfile.read().replace('\n', '')
    data_path = "/Users/iskrich/Desktop/diploma/BinaryTree/data/"
    instrument = stats.myStrategy.getInstrument()
    price = imgTemplate.format(source=data_path + "Price.png")
    strat = imgTemplate.format(source=data_path + "strat.png")
    indicators = ""
    for f in os.listdir("data"):
        if (f== ".DS_Store") or (f == "Price.png") or (f == "strat.png"):
            continue
        indicators += imgTemplate.format(source = data_path + f)

    outHtml = html.format(instrument = instrument, price = price, test_dates = test_dates, strat = strat,
                          indicators = indicators, result_dates = result_dates,
                          final_portfolio = stats.myStrategy.getResult(), cumulative = stats.retAnalyzer.getCumulativeReturns()[-1] * 100,
                          sharpe = stats.sharpeRatioAnalyzer.getSharpeRatio(0.05), max_drawdown = stats.drawDownAnalyzer.getMaxDrawDown() * 100,
                          total = stats.tradesAnalyzer.getCount(), average_profit = stats.tradesAnalyzer.getAll().mean(),
                          profits_std = stats.tradesAnalyzer.getAll().mean().std(), max_profit = stats.tradesAnalyzer.getAll().max(),
                          min_profit = stats.tradesAnalyzer.getAll().min(), profit_trades = stats.tradesAnalyzer.getProfitableCount(),
                          unprofit_trades = stats.tradesAnalyzer.getUnprofitableCount()
                          )
    print outHtml
    pdfkit.from_string(outHtml, 'docs/report.pdf', options=options)