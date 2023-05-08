import math
import schedule
from UIElements.StrategyTabAbstract import *
from Helpers.ScheduleHelper import *
import re
from Helpers.TickerReader import *
from Models.ORMModels import *


class PositionTab(StrategyTabAbstract):
    current_pos = []
    combo_legs = []
    total_avg_cost = 0

    def __init__(self, parent=None):
        StrategyTabAbstract.__init__(self, parent)
        self.groupBox_4 = QtWidgets.QGroupBox(parent=self)
        self.groupBox_4.setGeometry(QtCore.QRect(470, 30, 411, 511))
        self.groupBox_4.setObjectName("groupBox_4")
        self.strangle_labelStatusInfo_11 = QtWidgets.QLabel(parent=self.groupBox_4)
        self.strangle_labelStatusInfo_11.setGeometry(QtCore.QRect(40, 340, 121, 16))
        self.strangle_labelStatusInfo_11.setObjectName("strangle_labelStatusInfo_11")
        self.input_close_profitRate = QtWidgets.QLineEdit(parent=self.groupBox_4)
        self.input_close_profitRate.setGeometry(QtCore.QRect(180, 340, 91, 21))
        self.input_close_profitRate.setObjectName("input_close_profitRate")
        self.strangle_labelStatusInfo_12 = QtWidgets.QLabel(parent=self.groupBox_4)
        self.strangle_labelStatusInfo_12.setGeometry(QtCore.QRect(40, 380, 121, 16))
        self.strangle_labelStatusInfo_12.setObjectName("strangle_labelStatusInfo_12")
        self.input_close_LostRate = QtWidgets.QLineEdit(parent=self.groupBox_4)
        self.input_close_LostRate.setGeometry(QtCore.QRect(180, 380, 91, 21))
        self.input_close_LostRate.setObjectName("input_close_LostRate")
        self.btn_close_now = QtWidgets.QPushButton(parent=self.groupBox_4)
        self.btn_close_now.setGeometry(QtCore.QRect(30, 420, 113, 32))
        self.btn_close_now.setObjectName("btn_close_now")
        self.btn_save_autoClose = QtWidgets.QPushButton(parent=self.groupBox_4)
        self.btn_save_autoClose.setGeometry(QtCore.QRect(150, 420, 113, 32))
        self.btn_save_autoClose.setObjectName("btn_save_autoClose")
        self.label_7 = QtWidgets.QLabel(parent=self.groupBox_4)
        self.label_7.setGeometry(QtCore.QRect(40, 110, 85, 21))
        self.label_7.setObjectName("label_7")
        self.input_close_priceDiff = QtWidgets.QLineEdit(parent=self.groupBox_4)
        self.input_close_priceDiff.setGeometry(QtCore.QRect(110, 140, 71, 21))
        self.input_close_priceDiff.setObjectName("input_close_priceDiff")
        self.label_13 = QtWidgets.QLabel(parent=self.groupBox_4)
        self.label_13.setGeometry(QtCore.QRect(40, 140, 61, 21))
        self.label_13.setObjectName("label_13")
        self.input_close_price = QtWidgets.QLineEdit(parent=self.groupBox_4)
        self.input_close_price.setGeometry(QtCore.QRect(110, 170, 71, 21))
        self.input_close_price.setObjectName("input_close_price")
        self.label_16 = QtWidgets.QLabel(parent=self.groupBox_4)
        self.label_16.setGeometry(QtCore.QRect(40, 170, 61, 21))
        self.label_16.setObjectName("label_16")
        self.input_close_time = QtWidgets.QLineEdit(parent=self.groupBox_4)
        self.input_close_time.setGeometry(QtCore.QRect(110, 110, 71, 21))
        self.input_close_time.setObjectName("input_close_time")
        self.check_custom_close_price = QtWidgets.QCheckBox(parent=self.groupBox_4)
        self.check_custom_close_price.setGeometry(QtCore.QRect(200, 170, 131, 20))
        self.check_custom_close_price.setChecked(False)
        self.check_custom_close_price.setObjectName("check_custom_close_price")
        self.btn_refresh_close_price = QtWidgets.QPushButton(parent=self.groupBox_4)
        self.btn_refresh_close_price.setGeometry(QtCore.QRect(40, 240, 113, 32))
        self.btn_refresh_close_price.setObjectName("btn_refresh_close_price")
        self.label_close_bid = QtWidgets.QLabel(parent=self.groupBox_4)
        self.label_close_bid.setGeometry(QtCore.QRect(40, 200, 71, 21))
        self.label_close_bid.setObjectName("label_close_bid")
        self.label_close_ask = QtWidgets.QLabel(parent=self.groupBox_4)
        self.label_close_ask.setGeometry(QtCore.QRect(300, 200, 91, 21))
        self.label_close_ask.setObjectName("label_close_ask")
        self.label_close_midprice = QtWidgets.QLabel(parent=self.groupBox_4)
        self.label_close_midprice.setGeometry(QtCore.QRect(170, 200, 91, 21))
        self.label_close_midprice.setObjectName("label_close_midprice")
        self.btn_cancel_time_close = QtWidgets.QPushButton(parent=self.groupBox_4)
        self.btn_cancel_time_close.setGeometry(QtCore.QRect(150, 460, 113, 32))
        self.btn_cancel_time_close.setObjectName("btn_cancel_time_close")
        self.btn_cancel_rate_close = QtWidgets.QPushButton(parent=self.groupBox_4)
        self.btn_cancel_rate_close.setGeometry(QtCore.QRect(280, 460, 113, 32))
        self.btn_cancel_rate_close.setObjectName("btn_cancel_rate_close")
        self.btn_cancel_auto_close = QtWidgets.QPushButton(parent=self.groupBox_4)
        self.btn_cancel_auto_close.setGeometry(QtCore.QRect(280, 420, 113, 32))
        self.btn_cancel_auto_close.setObjectName("btn_cancel_auto_close")
        self.groupBox_7 = QtWidgets.QGroupBox(parent=self)
        self.groupBox_7.setGeometry(QtCore.QRect(30, 80, 401, 701))
        self.groupBox_7.setObjectName("groupBox_7")
        self.groupBox_8 = QtWidgets.QGroupBox(parent=self.groupBox_7)
        self.groupBox_8.setGeometry(QtCore.QRect(20, 40, 351, 251))
        self.groupBox_8.setObjectName("groupBox_8")
        self.position_stock_name = QtWidgets.QLabel(parent=self.groupBox_8)
        self.position_stock_name.setGeometry(QtCore.QRect(20, 40, 161, 21))
        self.position_stock_name.setObjectName("position_stock_name")
        self.position_stock_qty = QtWidgets.QLabel(parent=self.groupBox_8)
        self.position_stock_qty.setGeometry(QtCore.QRect(200, 40, 41, 21))
        self.position_stock_qty.setObjectName("position_stock_qty")
        self.position_leg1_name = QtWidgets.QLabel(parent=self.groupBox_8)
        self.position_leg1_name.setGeometry(QtCore.QRect(20, 70, 161, 21))
        self.position_leg1_name.setObjectName("position_leg1_name")
        self.position_leg1_qty = QtWidgets.QLabel(parent=self.groupBox_8)
        self.position_leg1_qty.setGeometry(QtCore.QRect(200, 70, 41, 21))
        self.position_leg1_qty.setObjectName("position_leg1_qty")
        self.position_stock_cost = QtWidgets.QLabel(parent=self.groupBox_8)
        self.position_stock_cost.setGeometry(QtCore.QRect(260, 40, 85, 21))
        self.position_stock_cost.setObjectName("position_stock_cost")
        self.position_leg1_cost = QtWidgets.QLabel(parent=self.groupBox_8)
        self.position_leg1_cost.setGeometry(QtCore.QRect(260, 70, 85, 21))
        self.position_leg1_cost.setObjectName("position_leg1_cost")
        self.position_leg2_name = QtWidgets.QLabel(parent=self.groupBox_8)
        self.position_leg2_name.setGeometry(QtCore.QRect(20, 100, 161, 21))
        self.position_leg2_name.setObjectName("position_leg2_name")
        self.position_leg2_qty = QtWidgets.QLabel(parent=self.groupBox_8)
        self.position_leg2_qty.setGeometry(QtCore.QRect(200, 100, 41, 21))
        self.position_leg2_qty.setObjectName("position_leg2_qty")
        self.position_leg2_cost = QtWidgets.QLabel(parent=self.groupBox_8)
        self.position_leg2_cost.setGeometry(QtCore.QRect(260, 100, 85, 21))
        self.position_leg2_cost.setObjectName("position_leg2_cost")
        self.position_leg3_name = QtWidgets.QLabel(parent=self.groupBox_8)
        self.position_leg3_name.setGeometry(QtCore.QRect(20, 130, 161, 21))
        self.position_leg3_name.setObjectName("position_leg3_name")
        self.position_leg4_name = QtWidgets.QLabel(parent=self.groupBox_8)
        self.position_leg4_name.setGeometry(QtCore.QRect(20, 160, 161, 21))
        self.position_leg4_name.setObjectName("position_leg4_name")
        self.position_total_cost = QtWidgets.QLabel(parent=self.groupBox_8)
        self.position_total_cost.setGeometry(QtCore.QRect(20, 190, 121, 21))
        self.position_total_cost.setObjectName("position_total_cost")
        self.position_current_marketValue = QtWidgets.QLabel(parent=self.groupBox_8)
        self.position_current_marketValue.setGeometry(QtCore.QRect(160, 190, 161, 21))
        self.position_current_marketValue.setObjectName("position_current_marketValue")
        self.position_leg3_qty = QtWidgets.QLabel(parent=self.groupBox_8)
        self.position_leg3_qty.setGeometry(QtCore.QRect(200, 130, 41, 21))
        self.position_leg3_qty.setObjectName("position_leg3_qty")
        self.position_leg4_qty = QtWidgets.QLabel(parent=self.groupBox_8)
        self.position_leg4_qty.setGeometry(QtCore.QRect(200, 160, 41, 21))
        self.position_leg4_qty.setObjectName("position_leg4_qty")
        self.position_leg4_cost = QtWidgets.QLabel(parent=self.groupBox_8)
        self.position_leg4_cost.setGeometry(QtCore.QRect(260, 160, 85, 21))
        self.position_leg4_cost.setObjectName("position_leg4_cost")
        self.position_leg3_cost = QtWidgets.QLabel(parent=self.groupBox_8)
        self.position_leg3_cost.setGeometry(QtCore.QRect(260, 130, 85, 21))
        self.position_leg3_cost.setObjectName("position_leg3_cost")
        self.position_profit = QtWidgets.QLabel(parent=self.groupBox_8)
        self.position_profit.setGeometry(QtCore.QRect(20, 220, 121, 21))
        self.position_profit.setObjectName("position_profit")
        self.position_id = QtWidgets.QLabel(parent=self.groupBox_8)
        self.position_id.setGeometry(QtCore.QRect(160, 220, 171, 21))
        self.position_id.setText("")
        self.position_id.setObjectName("position_id")
        self.btn_get_position = QtWidgets.QPushButton(parent=self)
        self.btn_get_position.setGeometry(QtCore.QRect(30, 30, 113, 32))
        self.btn_get_position.setObjectName("btn_get_position")
        self.retranslateUi()
        self.connectEvents()

    def connectEvents(self):
        self.btn_close_now.clicked.connect(self.btn_close_now_clicked)
        self.btn_get_position.clicked.connect(self.get_positions)
        self.btn_save_autoClose.clicked.connect(self.btn_schedule_clicked)
        self.btn_refresh_close_price.clicked.connect(self.refresh_price_clicked)
        self.btn_cancel_auto_close.clicked.connect(self.cancel_all_schedule)
        self.btn_cancel_rate_close.clicked.connect(self.cancel_rate_order)
        self.btn_cancel_time_close.clicked.connect(self.cancel_schedule_close_order)
        self.check_custom_close_price.setChecked(False)

    def onTickersEvent(self, tickers):
        if self.ticker is None:
            return

    def btn_close_now_clicked(self):
        self.get_positions()
        if self.current_pos is None or len(self.current_pos) <= 0:
            self.show_alert("no position to close")
            return

        self.refresh_price_clicked()
        lmt_price = round(float(self.input_close_price.text()), 2)
        if len(self.combo_legs) == 1:
            contract = self.sell_tickers[0].contract if len(self.buy_tickers) <= 0 else self.buy_tickers[0].contract
            act = "SELL" if len(self.buy_tickers) <= 0 else "BUY"
            combo_order = Order(action=act, orderType="LMT", tif="DAY")
            lmt_price = -lmt_price if act == "SELL" else lmt_price
        else:
            contract = Contract(secType="BAG", exchange="SMART")
            contract.symbol = self.current_pos[0].contract.symbol
            contract.currency = self.current_pos[0].contract.currency
            contract.comboLegs = self.combo_legs
            combo_order = Order(action="BUY", orderType="LMT", tif="DAY")

        combo_order.totalQuantity = math.fabs(self.current_pos[0].position)
        combo_order.tif = "DAY"  # the order is good till day end
        combo_order.discretionaryAmt = 0.02
        combo_order.percentOffset = 0.02

        if self.check_custom_close_price.isChecked():
            my_price = round(float(self.input_close_price.text()), 2)
            if math.fabs(my_price - lmt_price) > 0.5:
                self.show_alert("自定义价格与中间价差距过大，自动中间价下单")
            else:
                lmt_price = my_price

        self.input_close_price.setText(f"{lmt_price}")
        combo_order.lmtPrice = lmt_price

        if math.isnan(lmt_price):
            self.show_alert("无法获取有效报价数据，请关闭其他客户端重新连接")
            return

        self.current_trade = self.ib.placeOrder(contract, combo_order)
        i = 0
        retry_count = 3
        while i < retry_count:
            self.ib.sleep(3)
            if self.current_trade.isDone():
                break
            i += 1

            if len(self.buy_tickers) <= 0 and len(self.sell_tickers) <= 0:
                self.ib.cancelOrder(combo_order)
                return

            [lmt_price, ask, bid] = self.get_lmt_price(self.buy_tickers, self.sell_tickers)
            lmt_price = round(lmt_price+0.015*i, 2)
            if math.fabs(lmt_price-combo_order.lmtPrice) > 0.01:
                self.input_close_price.setText(f"{lmt_price}")
                combo_order.lmtPrice = lmt_price
                self.current_trade = self.ib.placeOrder(contract, combo_order)

        self.ib.sleep(5)
        if self.current_trade.orderStatus.status == OrderStatus.Filled:
            schedule.clear(ScheduleHelper.type_check_close_rate)
            schedule.clear(ScheduleHelper.type_close_order)
            self.save_close_finished()
        elif self.current_trade.isActive():
            self.ib.cancelOrder(combo_order)

    def refresh_price_clicked(self):
        if len(self.current_pos) <= 0:
            self.show_alert("没有可用持仓")
            return

        self.combo_legs = []
        self.buy_tickers = []
        self.sell_tickers = []
        self.total_avg_cost = 0
        for pos in self.current_pos:
            leg = ComboLeg()
            leg.conId = pos.contract.conId
            leg.ratio = 1
            leg.action = "SELL" if pos.position > 0 else "BUY"
            leg.exchange = pos.contract.exchange = "SMART"

            if leg.action == "BUY":
                self.total_avg_cost -= pos.avgCost / 100.0
                self.buy_tickers.append(self.ib.reqMktData(pos.contract, "", False, False, []))
            else:
                self.total_avg_cost += pos.avgCost / 100.0
                self.sell_tickers.append(self.ib.reqMktData(pos.contract, "", False, False, []))
            self.combo_legs.append(leg)

        self.ib.sleep(2)
        [lmt_price, ask, bid] = self.get_lmt_price(self.buy_tickers, self.sell_tickers)
        self.update_price_ask_bid_label(lmt_price, ask, bid)

        [profit, ratio] = self.get_position_pl(lmt_price, self.total_avg_cost)

        self.position_total_cost.setText(f"成本 {math.fabs(round(self.total_avg_cost, 2))} ")
        self.position_profit.setText(f"利润 {round(profit,2)} ")
        self.position_current_marketValue.setText(f"市场中间价 {lmt_price} ")
        self.position_id.setText(f"盈利比例 {round(ratio,2)}")

    def get_positions(self):
        if self.ib is None or not self.ib.isConnected():
            self.show_alert("链接已断开")
            return

        self.current_pos = []
        account_pos = self.ib.reqPositions()
        if account_pos is None or len(account_pos) <= 0:
            self.show_alert("没有持仓信息")
            return

        query = ORMHelper.session.query(OrderModel)
        option_pos = []
        stock_pos = None
        for con in account_pos:
            pos = query.filter(OrderModel.con_id == con.contract.conId, OrderModel.is_open == 1).first()
            if pos is not None:
                self.current_pos.append(con)
                pos.position = con.position
                pos.avg_cost = con.avgCost
                if pos.secType == "OPT":
                    option_pos.append(pos)
                else:
                    stock_pos = pos

        if len(self.current_pos) <= 0:
            self.show_alert("没有持仓信息")
            return
        ORMHelper.session.commit()

        label_names = self.position_leg1_name,self.position_leg2_name,self.position_leg3_name,self.position_leg4_name
        label_qtys = self.position_leg1_qty,self.position_leg2_qty,self.position_leg3_qty,self.position_leg4_qty
        label_costs = self.position_leg1_cost,self.position_leg2_cost,self.position_leg3_cost,self.position_leg4_cost

        for idx, pos in enumerate(option_pos):
            label_names[idx].setText(f"{pos.strike} {pos.symbol} {pos.lastTradeDate}")
            label_qtys[idx].setText(f"{pos.position}")
            label_costs[idx].setText(f"{pos.avg_cost}")

        if stock_pos is not None:
            self.position_stock_name.setText(stock_pos.symbol)
            self.position_stock_qty.setText(stock_pos.position)

    def save_close_finished(self):
        for c in self.buy_tickers:
            self.ib.cancelMktData(c.contract)
        for c in self.sell_tickers:
            self.ib.cancelMktData(c.contract)

        query = ORMHelper.session.query(OrderModel)
        for con in self.current_pos:
            pos = query.filter(OrderModel.con_id == con.contract.conId, OrderModel.is_open == 1).first()
            if pos is not None:
                pos.is_open = 0
        ORMHelper.session.commit()
        self.buy_tickers = self.sell_tickers = self.current_pos = []

    def btn_schedule_clicked(self):
        schedule.clear(ScheduleHelper.type_close_order)
        txt = self.input_close_time.text().strip()
        reg = re.compile(r'^\d{2}:\d{2}:\d{2}')
        if not reg.match(txt):
            self.show_alert("请正确输入定时时间")
            return False
        # sc_time = datetime.datetime.strptime(txt, "%")
        # 如果时间小于现在，则定时到明天
        ScheduleHelper.schedule_repeat_forever(self.check_pl_rate, 60)
        ScheduleHelper.schedule_job_at(self.btn_close_now_clicked, txt, ScheduleHelper.type_close_order)
        self.show_alert("定时任务成功")

    def check_pl_rate(self):
        self.refresh_price_clicked()

        if (len(self.buy_tickers) > 0 or len(self.sell_tickers) > 0) and self.total_avg_cost != 0:
            [lmt_price, ask, bid] = self.get_lmt_price(self.buy_tickers, self.sell_tickers)
            [profit, ratio] = self.get_position_pl(lmt_price, self.total_avg_cost)

            profit_rate_limit = lost_rate_limit = 0
            txt = self.input_close_profitRate.text()
            if self.check_input_is_number(txt):
                profit_rate_limit = float(txt)
            txt = self.input_close_LostRate.text()
            if self.check_input_is_number(txt):
                lost_rate_limit = -float(txt)

            if (profit_rate_limit != 0 and ratio >= lost_rate_limit) or \
                    (lost_rate_limit != 0 and ratio <= lost_rate_limit):
                self.btn_close_now_clicked()

    def update_price_ask_bid_label(self, price, ak, bd):
        self.input_close_price.setText(f"{price}")
        self.label_close_ask.setText(f"{ak}")
        self.label_close_bid.setText(f"{bd}")
        self.label_close_midprice.setText(f"{price}")

    def cancel_all_schedule(self):
        schedule.clear(ScheduleHelper.type_check_close_rate)
        schedule.clear(ScheduleHelper.type_close_order)

    def cancel_rate_order(self):
        schedule.clear(ScheduleHelper.type_check_close_rate)

    def cancel_schedule_close_order(self):
        schedule.clear(ScheduleHelper.type_close_order)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.groupBox_4.setTitle(_translate("MainWindow", "平仓信息"))
        self.strangle_labelStatusInfo_11.setText(_translate("MainWindow", "自动平仓Profit Rate"))
        self.input_close_profitRate.setText(_translate("MainWindow", "0.20"))
        self.strangle_labelStatusInfo_12.setText(_translate("MainWindow", "自动平仓Lost Rate"))
        self.input_close_LostRate.setText(_translate("MainWindow", "0.30"))
        self.btn_close_now.setText(_translate("MainWindow", "立即平仓"))
        self.btn_save_autoClose.setText(_translate("MainWindow", "开启自动平仓"))
        self.label_7.setText(_translate("MainWindow", "执行时间"))
        self.input_close_priceDiff.setText(_translate("MainWindow", "0.03"))
        self.label_13.setText(_translate("MainWindow", "下单价差"))
        self.input_close_price.setText(_translate("MainWindow", "1"))
        self.label_16.setText(_translate("MainWindow", "平仓金额"))
        self.input_close_time.setText(_translate("MainWindow", "21:35:55"))
        self.check_custom_close_price.setText(_translate("MainWindow", "使用自定义金额"))
        self.btn_refresh_close_price.setText(_translate("MainWindow", "刷新价格"))
        self.label_close_bid.setText(_translate("MainWindow", "买一"))
        self.label_close_ask.setText(_translate("MainWindow", "卖一"))
        self.label_close_midprice.setText(_translate("MainWindow", "中间"))
        self.btn_cancel_time_close.setText(_translate("MainWindow", "取消定时平仓"))
        self.btn_cancel_rate_close.setText(_translate("MainWindow", "取消盈利平仓"))
        self.btn_cancel_auto_close.setText(_translate("MainWindow", "取消自动平仓"))
        self.groupBox_7.setTitle(_translate("MainWindow", "持仓"))
        self.groupBox_8.setTitle(_translate("MainWindow", "订单"))
        self.position_stock_name.setText(_translate("MainWindow", "股票"))
        self.position_stock_qty.setText(_translate("MainWindow", "数量"))
        self.position_leg1_name.setText(_translate("MainWindow", "Leg1 "))
        self.position_leg1_qty.setText(_translate("MainWindow", "数量"))
        self.position_stock_cost.setText(_translate("MainWindow", "金额"))
        self.position_leg1_cost.setText(_translate("MainWindow", "金额"))
        self.position_leg2_name.setText(_translate("MainWindow", "Leg2"))
        self.position_leg2_qty.setText(_translate("MainWindow", "Leg1 "))
        self.position_leg2_cost.setText(_translate("MainWindow", "Leg1 "))
        self.position_leg3_name.setText(_translate("MainWindow", "Leg3"))
        self.position_leg4_name.setText(_translate("MainWindow", "Leg4"))
        self.position_total_cost.setText(_translate("MainWindow", "总成本"))
        self.position_current_marketValue.setText(_translate("MainWindow", "当前市场价值"))
        self.position_leg3_qty.setText(_translate("MainWindow", "Leg3"))
        self.position_leg4_qty.setText(_translate("MainWindow", "Leg3"))
        self.position_leg4_cost.setText(_translate("MainWindow", "Leg3"))
        self.position_leg3_cost.setText(_translate("MainWindow", "Leg3"))
        self.position_profit.setText(_translate("MainWindow", "当前盈亏"))
        self.btn_get_position.setText(_translate("MainWindow", "获取持仓"))

