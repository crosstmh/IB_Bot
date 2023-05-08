from PyQt6 import QtCore, QtGui, QtWidgets


class TickerTable(QtWidgets.QTableWidget):
    headers = [
        'symbol', 'delta', 'gamma', 'theta', 'impliedVol',
        'optPrice', 'vega','ask','bid']

    def __init__(self, parent=None):
        QtWidgets.QTableWidget.__init__(self, parent)
        self.conId2Row = {}
        self.setColumnCount(len(self.headers))
        self.setHorizontalHeaderLabels(self.headers)
        self.setAlternatingRowColors(True)

    def __contains__(self, contract):
        assert contract.conId
        return contract.conId in self.conId2Row

    def addTickers(self, tickers=[]):
        for ticker in tickers:
            self.addTickerRow(ticker)

    def addTickerRow(self, ticker):
        row = self.rowCount()
        self.insertRow(row)
        self.conId2Row[ticker.contract.conId] = row
        for col in range(len(self.headers)):
            item = QtWidgets.QTableWidgetItem('-')
            self.setItem(row, col, item)
        #set tye first column value
        item = self.item(row, 0)
        item.setText(ticker.contract.symbol+str(ticker.contract.strike))
        self.resizeColumnsToContents()

    def clearTickers(self):
        self.setRowCount(0)
        self.conId2Row.clear()

    def updateTickerRow(self, ticker):
        if len(self.conId2Row.keys()) <= 0:
            return

        row = self.conId2Row[ticker.contract.conId]
        for col, header in enumerate(self.headers):
            if col == 0:
                continue
            item = self.item(row, col)
            val = getattr(ticker.modelGreeks, header)
            item.setText(format(round(val, 3), ".4g"))
