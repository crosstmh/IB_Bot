import math

import schedule

from UIElements.StrategyTabAbstract import *
from Helpers.ScheduleHelper import *
import re
from Helpers.TickerReader import *
from Models.ORMModels import *


class StrangleTab(StrategyTabAbstract):
    btns_group = []
    label_legs_iv = []
    label_legs_sum = []
    label_legs_strike = []
    label_legs_type = []
    group_leg_check_types = []
    group_leg_check_dict = []
    combo_leg_ticks = []
    input_legs_expire = []

    def __init__(self, parent=None):
        StrategyTabAbstract.__init__(self, parent)
        self.groupBox = QtWidgets.QGroupBox(parent=self)
        self.groupBox.setGeometry(QtCore.QRect(480, 10, 401, 261))
        self.groupBox.setObjectName("groupBox")
        self.label_6 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(20, 50, 85, 21))
        self.label_6.setObjectName("label_6")
        self.btn_order_now = QtWidgets.QPushButton(parent=self.groupBox)
        self.btn_order_now.setGeometry(QtCore.QRect(20, 200, 113, 32))
        self.btn_order_now.setObjectName("btn_order_now")
        self.input_scheculeTime = QtWidgets.QLineEdit(parent=self.groupBox)
        self.input_scheculeTime.setGeometry(QtCore.QRect(90, 50, 71, 21))
        self.input_scheculeTime.setObjectName("input_scheculeTime")
        self.label_5 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(200, 50, 71, 21))
        self.label_5.setObjectName("label_5")
        self.input_average_iv = QtWidgets.QLineEdit(parent=self.groupBox)
        self.input_average_iv.setGeometry(QtCore.QRect(270, 50, 71, 21))
        self.input_average_iv.setObjectName("input_average_iv")
        self.label_10 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_10.setGeometry(QtCore.QRect(20, 90, 61, 21))
        self.label_10.setObjectName("label_10")
        self.input_buy_quantity = QtWidgets.QLineEdit(parent=self.groupBox)
        self.input_buy_quantity.setGeometry(QtCore.QRect(90, 90, 71, 21))
        self.input_buy_quantity.setObjectName("input_buy_quantity")
        self.input_order_priceDiff = QtWidgets.QLineEdit(parent=self.groupBox)
        self.input_order_priceDiff.setGeometry(QtCore.QRect(270, 90, 71, 21))
        self.input_order_priceDiff.setObjectName("input_order_priceDiff")
        self.label_11 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_11.setGeometry(QtCore.QRect(210, 90, 61, 21))
        self.label_11.setObjectName("label_11")
        self.label_bid1 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_bid1.setGeometry(QtCore.QRect(20, 120, 61, 21))
        self.label_bid1.setObjectName("label_bid1")
        self.label_ask1 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_ask1.setGeometry(QtCore.QRect(280, 120, 61, 21))
        self.label_ask1.setObjectName("label_ask1")
        self.label_mid_price = QtWidgets.QLabel(parent=self.groupBox)
        self.label_mid_price.setGeometry(QtCore.QRect(150, 120, 61, 21))
        self.label_mid_price.setObjectName("label_mid_price")
        self.label_15 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_15.setGeometry(QtCore.QRect(20, 160, 61, 21))
        self.label_15.setObjectName("label_15")
        self.input_order_price = QtWidgets.QLineEdit(parent=self.groupBox)
        self.input_order_price.setGeometry(QtCore.QRect(90, 160, 61, 21))
        self.input_order_price.setObjectName("input_order_price")
        self.btn_order_schedule = QtWidgets.QPushButton(parent=self.groupBox)
        self.btn_order_schedule.setGeometry(QtCore.QRect(140, 200, 113, 32))
        self.btn_order_schedule.setObjectName("btn_order_schedule")
        self.check_custom_buy_price = QtWidgets.QCheckBox(parent=self.groupBox)
        self.check_custom_buy_price.setGeometry(QtCore.QRect(160, 160, 131, 20))
        self.check_custom_buy_price.setChecked(False)
        self.check_custom_buy_price.setObjectName("check_custom_buy_price")
        self.btn_check_legs = QtWidgets.QPushButton(parent=self.groupBox)
        self.btn_check_legs.setGeometry(QtCore.QRect(280, 155, 111, 32))
        self.btn_check_legs.setObjectName("btn_check_legs")
        self.groupBox_leg1 = QtWidgets.QGroupBox(parent=self)
        self.groupBox_leg1.setGeometry(QtCore.QRect(30, 280, 411, 241))
        self.groupBox_leg1.setObjectName("groupBox_leg1")
        self.strangle_labelStatus_2 = QtWidgets.QLabel(parent=self.groupBox_leg1)
        self.strangle_labelStatus_2.setGeometry(QtCore.QRect(30, 50, 71, 22))
        self.strangle_labelStatus_2.setObjectName("strangle_labelStatus_2")
        self.strangle_labelStatusInfo_2 = QtWidgets.QLabel(parent=self.groupBox_leg1)
        self.strangle_labelStatusInfo_2.setGeometry(QtCore.QRect(30, 80, 81, 22))
        self.strangle_labelStatusInfo_2.setObjectName("strangle_labelStatusInfo_2")
        self.input_leg1_expire = QtWidgets.QLineEdit(parent=self.groupBox_leg1)
        self.input_leg1_expire.setGeometry(QtCore.QRect(120, 50, 81, 22))
        self.input_leg1_expire.setObjectName("input_leg1_expire")
        self.input_leg1_priceDiff = QtWidgets.QLineEdit(parent=self.groupBox_leg1)
        self.input_leg1_priceDiff.setGeometry(QtCore.QRect(120, 80, 81, 22))
        self.input_leg1_priceDiff.setObjectName("input_leg1_priceDiff")
        self.label_leg1_strike = QtWidgets.QLabel(parent=self.groupBox_leg1)
        self.label_leg1_strike.setGeometry(QtCore.QRect(230, 80, 121, 22))
        self.label_leg1_strike.setObjectName("label_leg1_strike")
        self.group_leg1_type = QtWidgets.QGroupBox(parent=self.groupBox_leg1)
        self.group_leg1_type.setGeometry(QtCore.QRect(20, 110, 321, 41))
        self.group_leg1_type.setTitle("")
        self.group_leg1_type.setObjectName("group_leg1_type")
        self.check_leg1_put = QtWidgets.QCheckBox(parent=self.group_leg1_type)
        self.check_leg1_put.setGeometry(QtCore.QRect(160, 10, 86, 20))
        self.check_leg1_put.setChecked(False)
        self.check_leg1_put.setObjectName("check_leg1_put")
        self.check_leg1_call = QtWidgets.QCheckBox(parent=self.group_leg1_type)
        self.check_leg1_call.setGeometry(QtCore.QRect(20, 10, 86, 20))
        self.check_leg1_call.setChecked(True)
        self.check_leg1_call.setObjectName("check_leg1_call")
        self.group_leg1_direction = QtWidgets.QGroupBox(parent=self.groupBox_leg1)
        self.group_leg1_direction.setGeometry(QtCore.QRect(20, 160, 321, 41))
        self.group_leg1_direction.setTitle("")
        self.group_leg1_direction.setObjectName("group_leg1_direction")
        self.check_leg1_short = QtWidgets.QCheckBox(parent=self.group_leg1_direction)
        self.check_leg1_short.setGeometry(QtCore.QRect(160, 10, 86, 20))
        self.check_leg1_short.setObjectName("check_leg1_short")
        self.check_leg1_long = QtWidgets.QCheckBox(parent=self.group_leg1_direction)
        self.check_leg1_long.setGeometry(QtCore.QRect(20, 10, 86, 20))
        self.check_leg1_long.setChecked(True)
        self.check_leg1_long.setObjectName("check_leg1_long")
        self.label_leg1_summary = QtWidgets.QLabel(parent=self.groupBox_leg1)
        self.label_leg1_summary.setGeometry(QtCore.QRect(20, 210, 361, 22))
        self.label_leg1_summary.setObjectName("label_leg1_summary")
        self.check_buy_leg1 = QtWidgets.QCheckBox(parent=self.groupBox_leg1)
        self.check_buy_leg1.setGeometry(QtCore.QRect(120, 25, 86, 20))
        self.check_buy_leg1.setChecked(True)
        self.check_buy_leg1.setObjectName("check_buy_leg1")
        self.strangle_labelStatus_22 = QtWidgets.QLabel(parent=self.groupBox_leg1)
        self.strangle_labelStatus_22.setGeometry(QtCore.QRect(30, 25, 71, 22))
        self.strangle_labelStatus_22.setObjectName("strangle_labelStatus_22")
        self.label_leg1_impliedVotality = QtWidgets.QLabel(parent=self.groupBox_leg1)
        self.label_leg1_impliedVotality.setGeometry(QtCore.QRect(230, 50, 131, 22))
        self.label_leg1_impliedVotality.setObjectName("label_leg1_impliedVotality")
        self.groupBox_leg2 = QtWidgets.QGroupBox(parent=self)
        self.groupBox_leg2.setGeometry(QtCore.QRect(470, 280, 411, 241))
        self.groupBox_leg2.setObjectName("groupBox_leg2")
        self.input_leg2_expire = QtWidgets.QLineEdit(parent=self.groupBox_leg2)
        self.input_leg2_expire.setGeometry(QtCore.QRect(130, 50, 81, 22))
        self.input_leg2_expire.setObjectName("input_leg2_expire")
        self.label_leg2_summary = QtWidgets.QLabel(parent=self.groupBox_leg2)
        self.label_leg2_summary.setGeometry(QtCore.QRect(30, 210, 351, 22))
        self.label_leg2_summary.setObjectName("label_leg2_summary")
        self.group_leg2_type = QtWidgets.QGroupBox(parent=self.groupBox_leg2)
        self.group_leg2_type.setGeometry(QtCore.QRect(30, 110, 321, 41))
        self.group_leg2_type.setTitle("")
        self.group_leg2_type.setObjectName("group_leg2_type")
        self.check_leg2_put = QtWidgets.QCheckBox(parent=self.group_leg2_type)
        self.check_leg2_put.setGeometry(QtCore.QRect(160, 10, 86, 20))
        self.check_leg2_put.setChecked(False)
        self.check_leg2_put.setObjectName("check_leg2_put")
        self.check_leg2_call = QtWidgets.QCheckBox(parent=self.group_leg2_type)
        self.check_leg2_call.setGeometry(QtCore.QRect(20, 10, 86, 20))
        self.check_leg2_call.setChecked(True)
        self.check_leg2_call.setObjectName("check_leg2_call")
        self.label_leg2_strike = QtWidgets.QLabel(parent=self.groupBox_leg2)
        self.label_leg2_strike.setGeometry(QtCore.QRect(240, 80, 71, 22))
        self.label_leg2_strike.setObjectName("label_leg2_strike")
        self.input_leg2_priceDiff = QtWidgets.QLineEdit(parent=self.groupBox_leg2)
        self.input_leg2_priceDiff.setGeometry(QtCore.QRect(130, 80, 81, 22))
        self.input_leg2_priceDiff.setObjectName("input_leg2_priceDiff")
        self.strangle_labelStatusInfo_4 = QtWidgets.QLabel(parent=self.groupBox_leg2)
        self.strangle_labelStatusInfo_4.setGeometry(QtCore.QRect(40, 80, 81, 22))
        self.strangle_labelStatusInfo_4.setObjectName("strangle_labelStatusInfo_4")
        self.strangle_labelStatus_13 = QtWidgets.QLabel(parent=self.groupBox_leg2)
        self.strangle_labelStatus_13.setGeometry(QtCore.QRect(40, 50, 71, 22))
        self.strangle_labelStatus_13.setObjectName("strangle_labelStatus_13")
        self.group_leg2_direction = QtWidgets.QGroupBox(parent=self.groupBox_leg2)
        self.group_leg2_direction.setGeometry(QtCore.QRect(30, 160, 321, 41))
        self.group_leg2_direction.setTitle("")
        self.group_leg2_direction.setObjectName("group_leg2_direction")
        self.check_leg2_short = QtWidgets.QCheckBox(parent=self.group_leg2_direction)
        self.check_leg2_short.setGeometry(QtCore.QRect(160, 10, 86, 20))
        self.check_leg2_short.setObjectName("check_leg2_short")
        self.check_leg2_long = QtWidgets.QCheckBox(parent=self.group_leg2_direction)
        self.check_leg2_long.setGeometry(QtCore.QRect(20, 10, 86, 20))
        self.check_leg2_long.setChecked(True)
        self.check_leg2_long.setObjectName("check_leg2_long")
        self.check_buy_leg2 = QtWidgets.QCheckBox(parent=self.groupBox_leg2)
        self.check_buy_leg2.setGeometry(QtCore.QRect(130, 25, 86, 20))
        self.check_buy_leg2.setChecked(True)
        self.check_buy_leg2.setObjectName("check_buy_leg2")
        self.strangle_labelStatus_21 = QtWidgets.QLabel(parent=self.groupBox_leg2)
        self.strangle_labelStatus_21.setGeometry(QtCore.QRect(40, 25, 71, 22))
        self.strangle_labelStatus_21.setObjectName("strangle_labelStatus_21")
        self.label_leg2_impliedVotality = QtWidgets.QLabel(parent=self.groupBox_leg2)
        self.label_leg2_impliedVotality.setGeometry(QtCore.QRect(240, 50, 131, 22))
        self.label_leg2_impliedVotality.setObjectName("label_leg2_impliedVotality")
        self.groupBox_leg3 = QtWidgets.QGroupBox(parent=self)
        self.groupBox_leg3.setGeometry(QtCore.QRect(30, 520, 411, 261))
        self.groupBox_leg3.setAutoFillBackground(False)
        self.groupBox_leg3.setObjectName("groupBox_leg3")
        self.check_buy_leg3 = QtWidgets.QCheckBox(parent=self.groupBox_leg3)
        self.check_buy_leg3.setGeometry(QtCore.QRect(130, 35, 86, 20))
        self.check_buy_leg3.setChecked(False)
        self.check_buy_leg3.setObjectName("check_buy_leg3")
        self.label_leg3_strike = QtWidgets.QLabel(parent=self.groupBox_leg3)
        self.label_leg3_strike.setGeometry(QtCore.QRect(240, 90, 71, 22))
        self.label_leg3_strike.setObjectName("label_leg3_strike")
        self.input_leg3_expire = QtWidgets.QLineEdit(parent=self.groupBox_leg3)
        self.input_leg3_expire.setGeometry(QtCore.QRect(130, 60, 81, 22))
        self.input_leg3_expire.setObjectName("input_leg3_expire")
        self.label_leg3_summary = QtWidgets.QLabel(parent=self.groupBox_leg3)
        self.label_leg3_summary.setGeometry(QtCore.QRect(30, 220, 311, 22))
        self.label_leg3_summary.setObjectName("label_leg3_summary")
        self.input_leg3_priceDiff = QtWidgets.QLineEdit(parent=self.groupBox_leg3)
        self.input_leg3_priceDiff.setGeometry(QtCore.QRect(130, 90, 81, 22))
        self.input_leg3_priceDiff.setObjectName("input_leg3_priceDiff")
        self.strangle_labelStatus_14 = QtWidgets.QLabel(parent=self.groupBox_leg3)
        self.strangle_labelStatus_14.setGeometry(QtCore.QRect(40, 60, 71, 22))
        self.strangle_labelStatus_14.setObjectName("strangle_labelStatus_14")
        self.strangle_labelStatus_25 = QtWidgets.QLabel(parent=self.groupBox_leg3)
        self.strangle_labelStatus_25.setGeometry(QtCore.QRect(40, 35, 71, 22))
        self.strangle_labelStatus_25.setObjectName("strangle_labelStatus_25")
        self.group_leg3_direction = QtWidgets.QGroupBox(parent=self.groupBox_leg3)
        self.group_leg3_direction.setGeometry(QtCore.QRect(30, 170, 321, 41))
        self.group_leg3_direction.setTitle("")
        self.group_leg3_direction.setObjectName("group_leg3_direction")
        self.check_leg3_short = QtWidgets.QCheckBox(parent=self.group_leg3_direction)
        self.check_leg3_short.setGeometry(QtCore.QRect(160, 10, 86, 20))
        self.check_leg3_short.setObjectName("check_leg3_short")
        self.check_leg3_long = QtWidgets.QCheckBox(parent=self.group_leg3_direction)
        self.check_leg3_long.setGeometry(QtCore.QRect(20, 10, 86, 20))
        self.check_leg3_long.setChecked(True)
        self.check_leg3_long.setObjectName("check_leg3_long")
        self.label_leg3_impliedVotality = QtWidgets.QLabel(parent=self.groupBox_leg3)
        self.label_leg3_impliedVotality.setGeometry(QtCore.QRect(240, 60, 121, 22))
        self.label_leg3_impliedVotality.setObjectName("label_leg3_impliedVotality")
        self.group_leg3_type = QtWidgets.QGroupBox(parent=self.groupBox_leg3)
        self.group_leg3_type.setGeometry(QtCore.QRect(30, 120, 321, 41))
        self.group_leg3_type.setTitle("")
        self.group_leg3_type.setObjectName("group_leg3_type")
        self.check_leg3_put = QtWidgets.QCheckBox(parent=self.group_leg3_type)
        self.check_leg3_put.setGeometry(QtCore.QRect(160, 10, 86, 20))
        self.check_leg3_put.setChecked(True)
        self.check_leg3_put.setObjectName("check_leg3_put")
        self.check_leg3_call = QtWidgets.QCheckBox(parent=self.group_leg3_type)
        self.check_leg3_call.setGeometry(QtCore.QRect(20, 10, 86, 20))
        self.check_leg3_call.setObjectName("check_leg3_call")
        self.strangle_labelStatusInfo_7 = QtWidgets.QLabel(parent=self.groupBox_leg3)
        self.strangle_labelStatusInfo_7.setGeometry(QtCore.QRect(40, 90, 81, 22))
        self.strangle_labelStatusInfo_7.setObjectName("strangle_labelStatusInfo_7")
        self.groupBox_leg4 = QtWidgets.QGroupBox(parent=self)
        self.groupBox_leg4.setGeometry(QtCore.QRect(470, 520, 411, 261))
        self.groupBox_leg4.setObjectName("groupBox_leg4")
        self.check_buy_leg4 = QtWidgets.QCheckBox(parent=self.groupBox_leg4)
        self.check_buy_leg4.setGeometry(QtCore.QRect(140, 35, 86, 20))
        self.check_buy_leg4.setChecked(False)
        self.check_buy_leg4.setObjectName("check_buy_leg4")
        self.label_leg4_strike = QtWidgets.QLabel(parent=self.groupBox_leg4)
        self.label_leg4_strike.setGeometry(QtCore.QRect(250, 90, 71, 22))
        self.label_leg4_strike.setObjectName("label_leg4_strike")
        self.input_leg4_expire = QtWidgets.QLineEdit(parent=self.groupBox_leg4)
        self.input_leg4_expire.setGeometry(QtCore.QRect(140, 60, 81, 22))
        self.input_leg4_expire.setObjectName("input_leg4_expire")
        self.label_leg4_summary = QtWidgets.QLabel(parent=self.groupBox_leg4)
        self.label_leg4_summary.setGeometry(QtCore.QRect(40, 220, 321, 22))
        self.label_leg4_summary.setObjectName("label_leg4_summary")
        self.input_leg4_priceDiff = QtWidgets.QLineEdit(parent=self.groupBox_leg4)
        self.input_leg4_priceDiff.setGeometry(QtCore.QRect(140, 90, 81, 22))
        self.input_leg4_priceDiff.setObjectName("input_leg4_priceDiff")
        self.strangle_labelStatus_15 = QtWidgets.QLabel(parent=self.groupBox_leg4)
        self.strangle_labelStatus_15.setGeometry(QtCore.QRect(50, 60, 71, 22))
        self.strangle_labelStatus_15.setObjectName("strangle_labelStatus_15")
        self.strangle_labelStatus_24 = QtWidgets.QLabel(parent=self.groupBox_leg4)
        self.strangle_labelStatus_24.setGeometry(QtCore.QRect(50, 35, 71, 22))
        self.strangle_labelStatus_24.setObjectName("strangle_labelStatus_24")
        self.group_leg4_direction = QtWidgets.QGroupBox(parent=self.groupBox_leg4)
        self.group_leg4_direction.setGeometry(QtCore.QRect(40, 170, 321, 41))
        self.group_leg4_direction.setTitle("")
        self.group_leg4_direction.setObjectName("group_leg4_direction")
        self.check_leg4_short = QtWidgets.QCheckBox(parent=self.group_leg4_direction)
        self.check_leg4_short.setGeometry(QtCore.QRect(160, 10, 86, 20))
        self.check_leg4_short.setObjectName("check_leg4_short")
        self.check_leg4_long = QtWidgets.QCheckBox(parent=self.group_leg4_direction)
        self.check_leg4_long.setGeometry(QtCore.QRect(20, 10, 86, 20))
        self.check_leg4_long.setChecked(True)
        self.check_leg4_long.setObjectName("check_leg4_long")
        self.label_leg4_impliedVotality = QtWidgets.QLabel(parent=self.groupBox_leg4)
        self.label_leg4_impliedVotality.setGeometry(QtCore.QRect(250, 60, 101, 22))
        self.label_leg4_impliedVotality.setObjectName("label_leg4_impliedVotality")
        self.group_leg4_type = QtWidgets.QGroupBox(parent=self.groupBox_leg4)
        self.group_leg4_type.setGeometry(QtCore.QRect(40, 120, 321, 41))
        self.group_leg4_type.setTitle("")
        self.group_leg4_type.setObjectName("group_leg4_type")
        self.check_leg4_put = QtWidgets.QCheckBox(parent=self.group_leg4_type)
        self.check_leg4_put.setGeometry(QtCore.QRect(160, 10, 86, 20))
        self.check_leg4_put.setChecked(True)
        self.check_leg4_put.setObjectName("check_leg4_put")
        self.check_leg4_call = QtWidgets.QCheckBox(parent=self.group_leg4_type)
        self.check_leg4_call.setGeometry(QtCore.QRect(20, 10, 86, 20))
        self.check_leg4_call.setObjectName("check_leg4_call")
        self.strangle_labelStatusInfo_5 = QtWidgets.QLabel(parent=self.groupBox_leg4)
        self.strangle_labelStatusInfo_5.setGeometry(QtCore.QRect(50, 90, 81, 22))
        self.strangle_labelStatusInfo_5.setObjectName("strangle_labelStatusInfo_5")
        self.groupBox_stock = QtWidgets.QGroupBox(parent=self)
        self.groupBox_stock.setGeometry(QtCore.QRect(30, 10, 421, 231))
        self.groupBox_stock.setObjectName("groupBox_stock")
        self.strangle_labelStatus_8 = QtWidgets.QLabel(parent=self.groupBox_stock)
        self.strangle_labelStatus_8.setGeometry(QtCore.QRect(30, 90, 60, 16))
        self.strangle_labelStatus_8.setObjectName("strangle_labelStatus_8")
        self.strangle_labelStatusInfo_8 = QtWidgets.QLabel(parent=self.groupBox_stock)
        self.strangle_labelStatusInfo_8.setGeometry(QtCore.QRect(30, 120, 281, 16))
        self.strangle_labelStatusInfo_8.setObjectName("strangle_labelStatusInfo_8")
        self.input_StockQuantity = QtWidgets.QLineEdit(parent=self.groupBox_stock)
        self.input_StockQuantity.setEnabled(False)
        self.input_StockQuantity.setGeometry(QtCore.QRect(140, 120, 81, 21))
        self.input_StockQuantity.setObjectName("input_StockQuantity")
        self.strangle_labelStatusInfo_9 = QtWidgets.QLabel(parent=self.groupBox_stock)
        self.strangle_labelStatusInfo_9.setGeometry(QtCore.QRect(30, 150, 281, 16))
        self.strangle_labelStatusInfo_9.setObjectName("strangle_labelStatusInfo_9")
        self.label_StockPrice = QtWidgets.QLabel(parent=self.groupBox_stock)
        self.label_StockPrice.setGeometry(QtCore.QRect(140, 90, 60, 16))
        self.label_StockPrice.setText("")
        self.label_StockPrice.setObjectName("label_StockPrice")
        self.btn_GetStock = QtWidgets.QPushButton(parent=self.groupBox_stock)
        self.btn_GetStock.setGeometry(QtCore.QRect(180, 20, 111, 31))
        self.btn_GetStock.setObjectName("btn_GetStock")
        self.input_StockCode = QtWidgets.QLineEdit(parent=self.groupBox_stock)
        self.input_StockCode.setGeometry(QtCore.QRect(30, 25, 131, 21))
        self.input_StockCode.setObjectName("input_StockCode")
        self.group_stock_type = QtWidgets.QGroupBox(parent=self.groupBox_stock)
        self.group_stock_type.setGeometry(QtCore.QRect(29, 180, 321, 41))
        self.group_stock_type.setTitle("")
        self.group_stock_type.setObjectName("group_stock_type")
        self.check_stock_put = QtWidgets.QCheckBox(parent=self.group_stock_type)
        self.check_stock_put.setGeometry(QtCore.QRect(160, 10, 86, 20))
        self.check_stock_put.setObjectName("check_stock_put")
        self.check_stock_call = QtWidgets.QCheckBox(parent=self.group_stock_type)
        self.check_stock_call.setGeometry(QtCore.QRect(20, 10, 86, 20))
        self.check_stock_call.setObjectName("check_stock_call")
        self.check_buy_stock = QtWidgets.QCheckBox(parent=self.groupBox_stock)
        self.check_buy_stock.setEnabled(False)
        self.check_buy_stock.setGeometry(QtCore.QRect(140, 60, 86, 20))
        self.check_buy_stock.setObjectName("check_buy_stock")
        self.strangle_labelStatus_23 = QtWidgets.QLabel(parent=self.groupBox_stock)
        self.strangle_labelStatus_23.setGeometry(QtCore.QRect(30, 60, 91, 22))
        self.strangle_labelStatus_23.setObjectName("strangle_labelStatus_23")
        self.label_stock_interestRate = QtWidgets.QLabel(parent=self.groupBox_stock)
        self.label_stock_interestRate.setGeometry(QtCore.QRect(140, 150, 60, 16))
        self.label_stock_interestRate.setObjectName("label_stock_interestRate")
        self.strangle_labelStatus_9 = QtWidgets.QLabel(parent=self)
        self.strangle_labelStatus_9.setGeometry(QtCore.QRect(30, 250, 71, 22))
        self.strangle_labelStatus_9.setObjectName("strangle_labelStatus_9")
        self.input_option_DTE_weeks = QtWidgets.QLineEdit(parent=self)
        self.input_option_DTE_weeks.setGeometry(QtCore.QRect(110, 250, 41, 22))
        self.input_option_DTE_weeks.setObjectName("input_option_DTE_weeks")
        self.btn_update_option_DTE = QtWidgets.QPushButton(parent=self)
        self.btn_update_option_DTE.setGeometry(QtCore.QRect(160, 245, 111, 32))
        self.btn_update_option_DTE.setObjectName("btn_update_option_DTE")
        self.retranslateUi()
        self.group_checkboxes()
        self.connectEvents()
        self.prepare_leg_elements()

    def group_checkboxes(self):
        self.check_custom_buy_price.setChecked(False)
        groups = [self.group_stock_type,self.group_leg1_type,self.group_leg1_direction,
                  self.group_leg2_type,self.group_leg2_direction,
                  self.group_leg3_type,self.group_leg3_direction,
                  self.group_leg4_type,self.group_leg4_direction]

        self.btns_group = []
        for g in groups:
            temp_box = QtWidgets.QButtonGroup()
            children = g.findChildren(QtWidgets.QCheckBox)
            for che in children:
                temp_box.addButton(che)
            temp_box.setExclusive(True)
            self.btns_group.append(temp_box)

    def prepare_leg_elements(self):
        self.input_legs_expire = self.input_leg1_expire, self.input_leg2_expire, self.input_leg3_expire, self.input_leg4_expire,
        self.label_legs_iv = self.label_leg1_impliedVotality, self.label_leg2_impliedVotality, self.label_leg3_impliedVotality, self.label_leg4_impliedVotality
        self.label_legs_type = self.label_leg1_impliedVotality, self.label_leg2_impliedVotality, self.label_leg3_impliedVotality, self.label_leg4_impliedVotality
        self.label_legs_strike = self.label_leg1_strike,self.label_leg2_strike,self.label_leg3_strike,self.label_leg4_strike
        self.label_legs_sum = self.label_leg1_summary,self.label_leg2_summary,self.label_leg3_summary,self.label_leg4_summary
        self.group_leg_check_types = self.group_leg1_type,self.group_leg2_type,self.group_leg3_type,self.group_leg4_type
        self.group_leg_check_dict = self.group_leg1_direction, self.group_leg2_direction, self.group_leg3_direction, self.group_leg4_direction

    def connectEvents(self):
        self.btn_GetStock.clicked.connect(self.get_stock_btn_clicked)
        self.btn_update_option_DTE.clicked.connect(self.update_dte_btn_clicked)
        self.input_leg1_priceDiff.editingFinished.connect(self.edit_price_diff_end)
        self.input_leg2_priceDiff.editingFinished.connect(self.edit_price_diff_end)
        self.input_leg3_priceDiff.editingFinished.connect(self.edit_price_diff_end)
        self.input_leg4_priceDiff.editingFinished.connect(self.edit_price_diff_end)
        self.btn_check_legs.clicked.connect(self.btn_check_legs_clicked)
        self.btn_order_now.clicked.connect(self.btn_order_now_clicked)
        self.btn_order_schedule.clicked.connect(self.btn_order_schedule_clicked)

    def get_stock_btn_clicked(self):
        if self.ib is None or not self.ib.isConnected():
            self.show_alert("请先点击连接客户端")
            return

        if self.ticker:
            self.ib.cancelMktData(self.ticker.contract)

        txt = self.input_StockCode.text().strip()
        if txt:
            self.getStockData(txt)
        else:
            self.show_alert("请输入美股代码")

    def update_dte_btn_clicked(self):
        txt = self.input_option_DTE_weeks.text().strip()
        if not self.check_input_is_number(txt):
            self.show_alert("请正确输入周数")
            return

        days = round(float(txt)) * 7
        self.getOptionData(days)
        if self.near_dte is None:
            self.show_alert("无法获取到过期日")
        elif len(self.calls) <= 0:
            self.show_alert("获取期权链数据失败")
        else:
            self.input_leg1_expire.setText(self.near_dte)
            self.input_leg2_expire.setText(self.near_dte)
            self.input_leg3_expire.setText(self.near_dte)
            self.input_leg4_expire.setText(self.near_dte)

    def edit_price_diff_end(self):
        input_ele = self.sender()
        label_ele = self.label_leg1_strike
        if "leg2" in input_ele.objectName():
            label_ele = self.label_leg2_strike
        elif "leg3" in input_ele.objectName():
            label_ele = self.label_leg3_strike
        elif "leg4" in input_ele.objectName():
            label_ele = self.label_leg4_strike

        txt = input_ele.text().strip()
        if not self.check_input_is_number(txt):
            self.show_alert("请正确输入正确价格距离")
            return
        s = self.getNearstStrike(int(txt))
        label_ele.setText(str(s))

    def check_buy_sell(self, group_box, is_action: bool = False):
        boxes = group_box.findChildren(QtWidgets.QCheckBox)
        result = ""
        for b in boxes:
            if b.isChecked():
                result = b.text()

        if not is_action:
            return result

        if result.lower() == "short":
            return "SELL"
        return "BUY"

    def btn_check_legs_clicked(self):
        self.pending_order = self.pending_contract = None
        self.combo_leg_ticks = []
        self.buy_tickers = []
        self.sell_tickers = []

        txt = self.input_StockQuantity.text().strip()
        if self.check_buy_stock.isChecked() and not self.check_input_is_number(txt):
            self.show_alert("请输入正确的股票份额")
            return
        stock_quantity = int(txt)

        txt = self.input_buy_quantity.text().strip()
        if not self.check_input_is_number(txt):
            self.show_alert("请输入正确的期权购买数量")
            return
        option_quantity = int(txt)

        txt = self.input_order_priceDiff.text().strip()
        if not self.check_input_is_number(txt):
            self.show_alert("请输入正确的下单价格偏差")
            return
        order_price_diff = round(float(txt), 3)

        combo_legs = []
        legs_needed = self.check_buy_leg1.isChecked(), self.check_buy_leg2.isChecked(), self.check_buy_leg3.isChecked(), self.check_buy_leg4.isChecked()

        if self.check_buy_stock.isChecked():
            pass
            # stock_leg = ComboLeg()
            # stock_leg.conId = self.ticker.contract.conId
            # stock_leg.ratio = stock_quantity
            # stock_leg.exchange = "SMART"
            # stock_leg.action = self.check_buy_sell(self.group_stock_type, True)
            #
            # mid_price = TickerReader.get_mid_price(self.ticker)
            # self.ticker.frozen_mid_price = round(mid_price, 3)
            # if math.isnan(mid_price) or mid_price <= 0:
            #     mid_price = self.ticker.marketPrice()
            # combo_legs.append(stock_leg)
            #
            # if stock_leg.action == "SELL":
            #     lmt_price -= mid_price
            # else:
            #     lmt_price += mid_price

        for idx, isNeed in enumerate(legs_needed):
            if isNeed:
                input_dte = self.input_legs_expire[idx]
                label_strike = self.label_legs_strike[idx]
                opt_type = self.check_buy_sell(self.group_leg_check_types[idx])
                leg_tmp_ticker = self.find_leg_ticker(label_strike.text(), opt_type, input_dte.text())

                if leg_tmp_ticker is None:
                    self.show_alert(f"leg{idx} 信息错误，请重试")
                    return
                label_iv = self.label_legs_iv[idx]
                label_sum = self.label_legs_sum[idx]

                mid_iv = round(TickerReader.get_mid_iv(leg_tmp_ticker), 3)
                mid_price = TickerReader.get_mid_price(leg_tmp_ticker)
                leg_tmp_ticker.froze_mid_price = mid_price
                label_iv.setText(f"iv: {mid_iv}")
                label_sum.setText(f"Sum:  M_Price: {mid_price}, {leg_tmp_ticker.contract.localSymbol}")

                leg_contract = ComboLeg()
                leg_contract.conId = leg_tmp_ticker.contract.conId
                leg_contract.ratio = 1
                leg_contract.action = self.check_buy_sell(self.group_leg_check_dict[idx], True)
                leg_contract.exchange = "SMART"
                combo_legs.append(leg_contract)
                self.combo_leg_ticks.append(leg_tmp_ticker)
                if leg_contract.action == "SELL":
                    self.sell_tickers.append(leg_tmp_ticker)
                else:
                    self.buy_tickers.append(leg_tmp_ticker)

        [lmt_price, ask, bid] = self.get_lmt_price(self.buy_tickers,self.sell_tickers)

        if len(combo_legs) <= 0:
            self.show_alert("未选择组合")
            return

        if len(combo_legs) == 1:
            contract = self.sell_tickers[0].contract if len(self.buy_tickers) <= 0 else self.buy_tickers[0].contract
            act = "SELL" if len(self.buy_tickers) <= 0 else "BUY"
            combo_order = Order(action=act, orderType="LMT", tif="DAY")
            lmt_price = -lmt_price if act == "SELL" else lmt_price
        else:
            contract = Contract(secType="BAG", exchange="SMART")
            contract.symbol = self.ticker.contract.symbol
            contract.currency = self.ticker.contract.currency
            contract.comboLegs = combo_legs
            combo_order = Order(action="BUY", orderType="LMT", tif="DAY")

        combo_order.totalQuantity = option_quantity
        combo_order.lmtPrice = round(lmt_price, 2)
        combo_order.discretionaryAmt = 0.02
        combo_order.percentOffset = 0.02

        self.update_price_ask_bid_label(lmt_price, ask, bid)
        self.pending_contract = contract
        self.pending_order = combo_order

    def onTickersEvent(self, tickers):
        if self.ticker is None:
            return

        for ticker in tickers:
            if ticker.contract.conId == self.ticker.contract.conId:
                self.update_stock_price_label(ticker)
            else:
                pass

    def btn_order_now_clicked(self):
        self.btn_cancel_current_clicked()

        self.btn_check_legs_clicked()
        if self.pending_order is None or self.pending_contract is None:
            self.show_alert("无法获取下单信息")
            return

        self.current_trade = self.ib.placeOrder(self.pending_contract, self.pending_order)
        schedule.clear(ScheduleHelper.type_place_order)

        i = 0
        self.repeat_count = 3
        while i < self.repeat_count:
            self.ib.sleep(5)
            if self.current_trade.isDone():
                break
            i += 1
            [lmt_price, ask, bid] = self.get_lmt_price(self.buy_tickers, self.sell_tickers)
            lmt_price = round(lmt_price + 0.015 * i, 2)
            if math.fabs(lmt_price - self.pending_order.lmtPrice) >= 0.015:
                self.update_price_ask_bid_label(lmt_price, ask, bid)
                self.pending_order.lmtPrice = lmt_price
                self.current_trade = self.ib.placeOrder(self.pending_contract, self.pending_order)

        self.ib.sleep(5)
        if self.current_trade.orderStatus.status == OrderStatus.Filled:
            schedule.clear(ScheduleHelper.type_place_order)
            self.order_filled()
        elif self.current_trade.isActive():
            self.ib.cancelOrder(self.pending_order)

    def btn_cancel_current_clicked(self):
        if self.current_trade is not None:
            if self.current_trade.isActive():
                self.ib.cancelOrder(self.current_trade.order)

            self.current_trade = self.pending_order = self.pending_contract = None
            self.combo_leg_ticks = []
            schedule.clear()

    def order_filled(self):
        createtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        trade_id = self.current_trade.contract.conId

        if self.check_buy_stock.isChecked():
            stock_order = OrderModel(secType="STK", con_id=self.ticker.contract.conId,avg_cost=self.ticker.frozen_mid_price,
                                     symbol=self.ticker.contract.symbol,createtime=createtime,action="BUY", trade_id=trade_id)
            ORMHelper.session.add(stock_order)

        for idx, leg in enumerate(self.combo_leg_ticks):
            act = self.check_buy_sell(self.group_leg_check_dict[idx], True)
            leg_order = OrderModel(secType="OPT", con_id=leg.contract.conId, action=act,
                                   lastTradeDate=leg.contract.lastTradeDateOrContractMonth, symbol=leg.contract.symbol,
                                   createtime=createtime, right=leg.contract.right, trade_id=trade_id,
                                   strike=leg.contract.strike, tradingClass=leg.contract.tradingClass)
            ORMHelper.session.add(leg_order)
        ORMHelper.session.commit()

    def btn_order_schedule_clicked(self):
        txt = self.input_scheculeTime.text().strip()
        reg = re.compile(r'^\d{2}:\d{2}:\d{2}')
        if not reg.match(txt):
            self.show_alert("请正确输入定时时间")
            return False
        # 如果时间小于现在，则定时到明天
        ScheduleHelper.schedule_job_at(self.btn_order_now_clicked, txt, ScheduleHelper.type_place_order)
        self.show_alert("定时任务成功")

    def update_price_ask_bid_label(self, price, ak, bd):
        self.input_order_price.setText(f"{price}")
        self.label_ask1.setText(f"{ak}")
        self.label_bid1.setText(f"{bd}")
        self.label_mid_price.setText(f"{price}")

    def update_stock_price_label(self, ticker):
        price = ticker.marketPrice()
        if math.isnan(price):
            price = ticker.close

        if math.isnan(price):
            price = ticker.last

        self.label_StockPrice.setText(str(price))

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.groupBox.setTitle(_translate("MainWindow", "开仓信息"))
        self.label_6.setText(_translate("MainWindow", "执行时间"))
        self.btn_order_now.setText(_translate("MainWindow", "立即下单"))
        self.input_scheculeTime.setText(_translate("MainWindow", "03:58:55"))
        self.label_5.setText(_translate("MainWindow", "平均IV低于"))
        self.input_average_iv.setText(_translate("MainWindow", "65"))
        self.label_10.setText(_translate("MainWindow", "执行数量"))
        self.input_buy_quantity.setText(_translate("MainWindow", "1"))
        self.input_order_priceDiff.setText(_translate("MainWindow", "0.02"))
        self.label_11.setText(_translate("MainWindow", "下单价差"))
        self.label_bid1.setText(_translate("MainWindow", "买一"))
        self.label_ask1.setText(_translate("MainWindow", "卖一"))
        self.label_mid_price.setText(_translate("MainWindow", "中间"))
        self.label_15.setText(_translate("MainWindow", "下单金额"))
        self.input_order_price.setText(_translate("MainWindow", "1"))
        self.btn_order_schedule.setText(_translate("MainWindow", "定时下单"))
        self.check_custom_buy_price.setText(_translate("MainWindow", "使用自定义金额"))
        self.btn_check_legs.setText(_translate("MainWindow", "刷新价格"))
        self.groupBox_leg1.setTitle(_translate("MainWindow", "leg1"))
        self.strangle_labelStatus_2.setText(_translate("MainWindow", "期权到期日"))
        self.strangle_labelStatusInfo_2.setText(_translate("MainWindow", "Strike距离"))
        self.input_leg1_expire.setText(_translate("MainWindow", "20230505"))
        self.input_leg1_priceDiff.setText(_translate("MainWindow", "3"))
        self.label_leg1_strike.setText(_translate("MainWindow", "185"))
        self.check_leg1_put.setText(_translate("MainWindow", "put"))
        self.check_leg1_call.setText(_translate("MainWindow", "call"))
        self.check_leg1_short.setText(_translate("MainWindow", "Short"))
        self.check_leg1_long.setText(_translate("MainWindow", "Long"))
        self.label_leg1_summary.setText(_translate("MainWindow", "Leg1 Infomation"))
        self.check_buy_leg1.setText(_translate("MainWindow", "Yes"))
        self.strangle_labelStatus_22.setText(_translate("MainWindow", "是否使用"))
        self.label_leg1_impliedVotality.setText(_translate("MainWindow", "iv"))
        self.groupBox_leg2.setTitle(_translate("MainWindow", "leg2"))
        self.input_leg2_expire.setText(_translate("MainWindow", "20230505"))
        self.label_leg2_summary.setText(_translate("MainWindow", "Leg2 Infomation"))
        self.check_leg2_put.setText(_translate("MainWindow", "put"))
        self.check_leg2_call.setText(_translate("MainWindow", "call"))
        self.label_leg2_strike.setText(_translate("MainWindow", "185"))
        self.input_leg2_priceDiff.setText(_translate("MainWindow", "-3"))
        self.strangle_labelStatusInfo_4.setText(_translate("MainWindow", "Strike距离"))
        self.strangle_labelStatus_13.setText(_translate("MainWindow", "期权到期日"))
        self.check_leg2_short.setText(_translate("MainWindow", "Short"))
        self.check_leg2_long.setText(_translate("MainWindow", "Long"))
        self.check_buy_leg2.setText(_translate("MainWindow", "Yes"))
        self.strangle_labelStatus_21.setText(_translate("MainWindow", "是否使用"))
        self.label_leg2_impliedVotality.setText(_translate("MainWindow", "iv"))
        self.groupBox_leg3.setTitle(_translate("MainWindow", "leg3"))
        self.check_buy_leg3.setText(_translate("MainWindow", "Yes"))
        self.label_leg3_strike.setText(_translate("MainWindow", "185"))
        self.input_leg3_expire.setText(_translate("MainWindow", "20230505"))
        self.label_leg3_summary.setText(_translate("MainWindow", "Leg3 Infomation"))
        self.input_leg3_priceDiff.setText(_translate("MainWindow", "3"))
        self.strangle_labelStatus_14.setText(_translate("MainWindow", "期权到期日"))
        self.strangle_labelStatus_25.setText(_translate("MainWindow", "是否使用"))
        self.check_leg3_short.setText(_translate("MainWindow", "Short"))
        self.check_leg3_long.setText(_translate("MainWindow", "Long"))
        self.label_leg3_impliedVotality.setText(_translate("MainWindow", "iv"))
        self.check_leg3_put.setText(_translate("MainWindow", "put"))
        self.check_leg3_call.setText(_translate("MainWindow", "call"))
        self.strangle_labelStatusInfo_7.setText(_translate("MainWindow", "Strike距离"))
        self.groupBox_leg4.setTitle(_translate("MainWindow", "leg4"))
        self.check_buy_leg4.setText(_translate("MainWindow", "Yes"))
        self.label_leg4_strike.setText(_translate("MainWindow", "185"))
        self.input_leg4_expire.setText(_translate("MainWindow", "20230505"))
        self.label_leg4_summary.setText(_translate("MainWindow", "Leg4 Infomation"))
        self.input_leg4_priceDiff.setText(_translate("MainWindow", "-3"))
        self.strangle_labelStatus_15.setText(_translate("MainWindow", "期权到期日"))
        self.strangle_labelStatus_24.setText(_translate("MainWindow", "是否使用"))
        self.check_leg4_short.setText(_translate("MainWindow", "Short"))
        self.check_leg4_long.setText(_translate("MainWindow", "Long"))
        self.label_leg4_impliedVotality.setText(_translate("MainWindow", "iv"))
        self.check_leg4_put.setText(_translate("MainWindow", "put"))
        self.check_leg4_call.setText(_translate("MainWindow", "call"))
        self.strangle_labelStatusInfo_5.setText(_translate("MainWindow", "Strike距离"))
        self.groupBox_stock.setTitle(_translate("MainWindow", "Stock"))
        self.strangle_labelStatus_8.setText(_translate("MainWindow", "当前价格"))
        self.strangle_labelStatusInfo_8.setText(_translate("MainWindow", "交易数量"))
        self.input_StockQuantity.setText(_translate("MainWindow", "100"))
        self.strangle_labelStatusInfo_9.setText(_translate("MainWindow", "卖空利率"))
        self.btn_GetStock.setText(_translate("MainWindow", "获取股价数据"))
        self.input_StockCode.setText(_translate("MainWindow", "TSLA"))
        self.input_StockCode.setPlaceholderText(_translate("MainWindow", "请输入股票"))
        self.check_stock_put.setText(_translate("MainWindow", "Short"))
        self.check_stock_call.setText(_translate("MainWindow", "Long"))
        self.check_buy_stock.setText(_translate("MainWindow", "Yes"))
        self.strangle_labelStatus_23.setText(_translate("MainWindow", "是否买卖股票"))
        self.label_stock_interestRate.setText(_translate("MainWindow", "Nan"))
        self.strangle_labelStatus_9.setText(_translate("MainWindow", "期权到期周"))
        self.input_option_DTE_weeks.setText(_translate("MainWindow", "1"))
        self.btn_update_option_DTE.setText(_translate("MainWindow", "确定"))
