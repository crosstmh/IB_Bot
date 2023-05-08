from datetime import *
from UIElements.TickerTable import *
from PyQt6.QtWidgets import QMessageBox
from Helpers.FileHelper import FileHelper
import re
from Helpers.TickerReader import *
from Models.CoreData import *


class StrategyTabAbstract(QtWidgets.QWidget):
    ib: IB = None
    stock = None  # stock contract
    ticker = None  # stock ticker data
    near_dte = None
    strikes = None
    current_trade: Trade = None
    pending_contract = None
    pending_order = None

    repeat_count = 3
    chain = []
    calls = []
    puts = []
    buy_tickers = []
    sell_tickers = []

    def __int__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

    def set_client(self, ib: IB):
        self.ib = ib
        self.ib.pendingTickersEvent += self.onTickersEvent
        self.ib.errorEvent += self.onError
        self.ib.orderStatusEvent += self.onOrderStatusEvent

    def show_alert(self, text=""):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Notice！")
        dlg.setText(text)
        dlg.exec()

    def reset_all_stock_relate_data(self):
        if self.ticker is not None:
            self.ib.cancelMktData(self.ticker.contract)
        self.near_dte = self.strikes = None
        self.calls = []
        self.puts = []
        self.chain = []
        self.buy_tickers = []
        self.sell_tickers = []
        self.pending_order = self.pending_contract = self.current_trade = None

    def getStockData(self, stock_code):
        text = stock_code
        contract = Stock(symbol=text, currency="USD", exchange="SMART",primaryExchange="NASDAQ")
        if contract and self.ib.qualifyContracts(contract):
            self.reset_all_stock_relate_data()
            self.stock = contract
            self.ticker = self.ib.reqMktData(contract, '', False, False, [])
            self.ib.sleep(2)

    def getNearstExpire(self, day_limit:int=0):
        chains = self.ib.reqSecDefOptParams(self.stock.symbol, '', self.stock.secType, self.stock.conId)
        chain = next(c for c in chains if c.tradingClass == self.stock.symbol and c.exchange == 'SMART')

        expirations = sorted(exp for exp in chain.expirations)
        day_diff = 9999
        target_exp = None
        for exp in expirations:
            d = datetime.strptime(exp, "%Y%m%d").date()
            days = self.dayDifference(d)
            if day_limit < days < day_diff:
                target_exp = exp
                day_diff = days

        self.near_dte = target_exp
        return target_exp

    def getNearstStrike(self,priceDiff:int):
        if len(self.calls) <= 0:
            self.show_alert("请先获取期权链数据")
            return

        price_value = self.ticker.marketPrice()
        if math.isnan(price_value):
            price_value = self.ticker.close
        if math.isnan(price_value):
            price_value = self.ticker.last

        result = None
        temp = 9999
        for call in self.calls:
            dist = (call.contract.strike - price_value)
            if 0 < priceDiff <= dist < temp:
                temp = priceDiff
                result = call.contract.strike
            elif 0 > priceDiff >= dist:
                result = call.contract.strike

        return result

    def getAvailStrikes(self, areaStep:int=30):
        price_value = self.ticker.marketPrice()
        if math.isnan(price_value):
            price_value = self.ticker.close
        if math.isnan(price_value):
            price_value = self.ticker.last

        chains = self.ib.reqSecDefOptParams(self.stock.symbol, '', self.stock.secType, self.stock.conId)
        chain = next(c for c in chains if c.tradingClass == self.stock.symbol and c.exchange == 'SMART')
        strikes = [strike for strike in chain.strikes
                   if price_value - areaStep < strike < price_value + areaStep]
        self.strikes = strikes
        return strikes

    def find_option_in_array(self, strike, ty: str = "call", expire:str = "20230526"):
        target_arr = self.calls
        if ty.lower() == "put":
            target_arr = self.puts
        for con in target_arr:
            if self.check_input_is_number(strike) and con.contract.strike == float(strike) \
                    and con.contract.lastTradeDateOrContractMonth == expire:
                return con
        return None

    def find_leg_ticker(self, strike, right, expire):
        leg_tmp_ticker = self.find_option_in_array(strike, right, expire)
        if leg_tmp_ticker is None:
            rt = "C" if right == "call" else "P"
            leg_tmp_ticker = self.verify_contract(self.ticker.contract.symbol, strike, expire,right=rt)

        return leg_tmp_ticker

    def verify_contract(self, symbol, strike, expire_date, right) -> Ticker:
        opt: Contract = Option(symbol, expire_date, strike, right, 'SMART', multiplier="100", tradingClass=symbol)
        temp_opt = self.ib.qualifyContracts(*[opt])
        ticker = None
        if len(temp_opt) <= 0:
            return ticker

        opt = temp_opt[0]
        if opt.conId != 0:
            ticker = self.ib.reqMktData(opt, '', False, False, [])
            target_arr = self.calls if right == "C" else self.puts
            already_in = False
            for t in target_arr:
                if t.contract.conId == ticker.contract.conId:
                    already_in = True
                    break

            if not already_in:
                self.ib.sleep(3)
                target_arr.append(ticker)
        return ticker

    def getOptionData(self, day_limit:int=7):
        if self.stock is None:
            self.show_alert("请先获取股票数据")
            return

        self.puts = []
        self.calls = []
        self.chain = []

        chains = self.ib.reqSecDefOptParams(self.stock.symbol, '', self.stock.secType, self.stock.conId)
        chain = next(c for c in chains if c.tradingClass == self.stock.symbol and c.exchange == 'SMART')
        if self.strikes is None or len(self.strikes) <= 0:
            self.getAvailStrikes()

        if self.near_dte is None:
            self.getNearstExpire(day_limit)

        strikes = self.strikes
        expirations = [self.near_dte]
        rights = ['P', 'C']

        p_contracts = [Option(self.stock.symbol, expiration, strike, rights[0], 'SMART', multiplier="100",
                              tradingClass=chain.tradingClass)
                       for expiration in expirations
                       for strike in strikes]
        c_contracts = [Option(self.stock.symbol, expiration, strike, rights[1], 'SMART', multiplier="100",
                              tradingClass=chain.tradingClass)
                       for expiration in expirations
                       for strike in strikes]

        p_contracts = self.ib.qualifyContracts(*p_contracts)

        for p in p_contracts:
            self.puts.append(self.ib.reqMktData(p, '', False, False, []))

        c_contracts = self.ib.qualifyContracts(*c_contracts)
        for c in c_contracts:
            self.calls.append(self.ib.reqMktData(c, '', False, False, []))

        self.chain = chain

    def onOrderStatusEvent(self, trade: Trade):
        pass


    def onError(self, errorId, errorCode, errorMsg, errorObject):
        ignore_codes = [200]
        # 201,103, 399, 202, 2119,2105,2106,2157,2158,2104,2103,2107
        print(errorCode)
        is_prev = CoreData.errorCode == errorCode
        if not isinstance(errorObject, Option) and errorCode not in ignore_codes and not is_prev:
            CoreData.errorCode = errorCode
            self.show_alert(errorMsg)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            fh = FileHelper()
            fh.write_log(f"{timestamp}  *  {errorCode}  *  {errorMsg}")

    def check_input_is_number(self, txt: str):
        reg = re.compile(r'\-{0,1}\d+\.{0,1}\d{0,}?')
        if reg.match(txt):
            return True
        return False

    def onTickersEvent(self, tickers):
        pass

    def get_position_pl(self, now_price, cost) -> [float, float]:
        profit = ratio = 0
        if cost < 0:
            profit = -(now_price + cost)
            ratio = -(profit / cost)
        elif cost > 0:
            profit = now_price - cost
            ratio = profit / cost

        return [profit, ratio]
    def get_lmt_price(self, buy_tickers, sell_tickers) -> [float, float, float]:
        lmt_price: float = 0
        ask: float = 0
        bid: float = 0
        for t in buy_tickers:
            temp_p = TickerReader.get_mid_price(t)
            lmt_price += temp_p
            ask += t.ask
            bid += t.bid

        for t in sell_tickers:
            temp_p = TickerReader.get_mid_price(t)
            lmt_price -= temp_p
            ask -= t.ask
            bid -= t.bid

        return [round(lmt_price,2), round(ask,2) , round(bid,2)]

    def replace_id_InList(self, ticker, arr:list):
        idx = -1
        for c in arr:
            if c.contract.conId == ticker.contract.conId:
                idx = arr.index(c)
                break
        if idx > 0:
            arr[idx] = ticker

    def dayDifference(self, end: date, now=datetime.now().date()):
        return (end - now).days
