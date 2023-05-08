from ib_insync import *
import math
from ib_insync.contract import *

class TickerReader:

    @staticmethod
    def get_ask_price(ticker: Ticker) -> float:
        if math.isnan(ticker.ask):
            if ticker.askGreeks is not None and ticker.askGreeks.optPrice is not None:
                return ticker.askGreeks.optPrice
        return ticker.ask

    @staticmethod
    def get_bid_price(ticker: Ticker) -> float:
        if math.isnan(ticker.bid):
            if ticker.bidGreeks is not None:
                return ticker.bidGreeks.optPrice
        return ticker.bid

    @staticmethod
    def get_last_price(ticker: Ticker) -> float:
        if math.isnan(ticker.last):
            if ticker.lastGreeks is not None and ticker.lastGreeks.optPrice is not None:
                return ticker.lastGreeks.optPrice
        return ticker.last

    @staticmethod
    def get_model_price(ticker: Ticker) -> float:
        if ticker.modelGreeks is not None and ticker.modelGreeks.optPrice is not None:
            return ticker.modelGreeks.optPrice
        return math.nan

    @staticmethod
    def get_mid_price(ticker: Ticker) -> float:
        if not math.isnan(ticker.ask) and not math.isnan(ticker.bid):
            if ticker.ask > 0 and ticker.bid > 0:
                return (ticker.ask + ticker.bid) / 2.0
        if ticker.bidGreeks is not None and ticker.askGreeks is not None and \
                ticker.bidGreeks.optPrice is not None and ticker.askGreeks.optPrice is not None:
            return (ticker.bidGreeks.optPrice + ticker.askGreeks.optPrice) / 2.0

        if not math.isnan(ticker.last):
            return ticker.last

        if not math.isnan(ticker.close):
            return ticker.close

        return math.nan

    @staticmethod
    def get_mid_iv(ticker: Ticker) -> float:
        if ticker.bidGreeks is not None and ticker.askGreeks is not None and \
                ticker.bidGreeks.impliedVol is not None and ticker.askGreeks.impliedVol is not None:
            return (ticker.bidGreeks.impliedVol+ticker.askGreeks.impliedVol)/2.0

        return math.nan

    @staticmethod
    def get_model_iv(ticker: Ticker) -> float:
        if ticker.modelGreeks is not None and \
                ticker.modelGreeks.impliedVol is not None:
            return ticker.modelGreeks.impliedVol
        return math.nan