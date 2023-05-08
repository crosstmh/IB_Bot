import numpy as np
from scipy.stats import norm

class BoxSpread:
    def calculate_option_pain(self,strikes=[]):
        pass

    def bull_put_spread(self,stock_price,T,r,shot_price,shot_strike,long_price,long_strike,quantity=1):
        transaction_costs = quantity * 0.65

        short_iv = self.implied_volatility(stock_price,shot_strike,T,r,shot_price,"put")

        # P&L calculation
        short_put_pl = max(stock_price - shot_strike, 0) * quantity - shot_price * quantity
        long_put_pl = max(long_strike - stock_price, 0) * quantity - long_price * quantity
        net_pl = short_put_pl + long_put_pl - transaction_costs

        break_even_price = (shot_strike + long_strike)/2
        z = (break_even_price - stock_price + shot_price) / (
                    stock_price * short_iv * np.sqrt(T))
        pop = norm.cdf(z)

        print("Net P&L: $"+ str(round(net_pl, 3))+"， Posisbility：" + str(round(pop,4)))

    def put_call_parity(self, S, K, T, r,call_price,put_price):
        # P + S = C + K * np.exp(-r * T)
        # 左侧是put + 股票， 右侧是call + strike*无风险利率
        # 计算后，卖出价格贵的一边，买入价格低的一边
        # 该公式，没有考虑 short stock 利率费用
        # Call premium - Put premium = Stock price - Strike price / (1 + risk-free rate)^time to expiration
        ib_fee = 0.65
        left = call_price - put_price
        right = S - K * np.exp(-r * T)
        # the fee not only consider this time but multiply by 2 for close position
        arbitrage_value = abs(left - right) * 100 - 2 * ib_fee

        #if the gap is less than 20 profit is two low
        if arbitrage_value < 20:
            return [False,"no chance"]
        if left < right:
            # sell put, short stock , buy call
            # shot stock fee is too high
            pass
        elif left > right:
            # buy put , buy stock , sell call
            pass

    def calculate_asym(self, strike, underlying_price, premium):
        asym = (2 * strike - underlying_price + premium) / underlying_price
        return asym

    def put_delta(self, S, K, T, r, sigma):
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        return -norm.cdf(-d1)

    # 定义计算期权隐含波动率的函数
    # S: 标的资产当前价格
    # K: 行权价格
    # r: 无风险利率
    # T: 剩余期限，以年为单位
    # option_price: 期权当前市场价格
    # option_type = "call", "put"
    def implied_volatility(self, S, K, T, r, option_price, option_type):
        # """
        # Calculates the implied volatility using the Black-Scholes model and the Newton-Raphson method
        # """
        tol = 1e-6
        sigma_i = 0.5
        for i in range(100):
            option_price_i = self.bsm_price(S, K, T, r, sigma_i, option_type)
            vega = S * norm.pdf(
                (np.log(S / K) + (r + 0.5 * sigma_i ** 2) * T) / (sigma_i * np.sqrt(T))) * np.sqrt(T)
            sigma_i -= (option_price_i - option_price) / vega
            if abs(option_price_i - option_price) < tol:
                return sigma_i
        return np.nan
