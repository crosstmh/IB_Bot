import datetime

import pandas as pd
import schedule
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMessageBox
from Models.IBClient import *
from UIElements.UIWindow import Ui_MainWindow
from Helpers.ScheduleHelper import *
from Helpers.BoxSpread import *
from ib_insync import util
# from PyQt6.QtCore import pyqtSlot


class WindowController(QtWidgets.QMainWindow,Ui_MainWindow):
    clientId = 124
    host = "127.0.0.1"
    ib = None
    ibClient = None
    ticker = None
    stock = None
    chain = None
    core = None
    schedule_timer = None

    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.label_schedule_open_summary.setText("无")
        self.label_schedule_close_summary.setText("无")
        self.ibClient = IBClient(self.host, self.inputPort.text(), self.clientId)
        self.ib = self.ibClient.ib
        self.check_schedule_job()
        self.connectAllEvents()

    def check_schedule_job(self):
        self.schedule_timer = QtCore.QTimer()
        self.schedule_timer.timeout.connect(ScheduleHelper.check_pending)
        self.schedule_timer.setInterval(5000)
        self.schedule_timer.start()

    def test_arbitrage(self):
        S = 48.05  # Current price of the underlying asset
        K = 42  # Strike price of the option
        r = 0.043  # Risk-free interest rate
        T = 28/365.0  # Time to expiration in years

        long_price = 0.72  # Price of the call option
        long_strike = 24
        short_price = 0.825  # Price of the put option
        short_strike = 24.5
        hel = BoxSpread()
        # re0 = hel.parity_arbitrage(S,K,T,r,call_price,put_price)

        # re1 = hel.puts_combined(22,T,r,short_price,short_strike,long_price,long_strike)
        # print(re1)


    def connectAllEvents(self):
        self.btnConnect.clicked.connect(self.btnConnectClicked)
        self.btn_get_all_schedule.clicked.connect(self.get_schedule_jobs)
        self.btn_cancel_all_schedule.clicked.connect(self.cancle_schedule_jobs)

    def btnConnectClicked(self):
        port = self.inputPort.text().strip()
        if port:
            self.ibClient.port = port
            flag = self.ibClient.try_connect()
            msg = "连接成功" if flag[0] else flag[1]

            if flag[0]:
                self.ib.reqMarketDataType(1)
                self.tab2.set_client(self.ib)
                self.tab3.set_client(self.ib)
        else:
            msg = "请输入端口号，默认为7496"
        self.show_alert(msg)

    def cancle_schedule_jobs(self):
        ScheduleHelper.cancel_all()
        self.label_schedule_open_summary.setText(f"无")
        self.label_schedule_close_summary.setText(f"无")

    def get_schedule_jobs(self):
        close_job = schedule.get_jobs(ScheduleHelper.type_close_order)
        order_job = schedule.get_jobs(ScheduleHelper.type_place_order)
        rate_close_job = schedule.get_jobs(ScheduleHelper.type_check_close_rate)

        order_job = order_job[0] if len(order_job) > 0 else None
        close_job = close_job[0] if len(close_job) > 0 else None
        rate_close_job = rate_close_job[0] if len(rate_close_job) > 0 else None

        if order_job is not None:
            open_time = order_job.next_run.strftime("%Y-%m-%d %H:%M:%S")
            self.label_schedule_open_summary.setText(f"任务将于 {open_time} 执行")
        else:
            self.label_schedule_open_summary.setText(f"无")

        if close_job is not None:
            close_time = close_job.next_run.strftime("%Y-%m-%d %H:%M:%S")
            self.label_schedule_close_summary.setText(f"任务将于 {close_time} 执行")
        else:
            self.label_schedule_close_summary.setText(f"无")

        if rate_close_job is not None:
            rate_time = rate_close_job.next_run.strftime("%Y-%m-%d %H:%M:%S")
            self.label_schedule_close_summary_2.setText(f"任务将于 {rate_time} 执行")
        else:
            self.label_schedule_close_summary_2.setText(f"无")

    def closeEvent(self, event):
        self.ib.disconnect()
        loop = util.getLoop()
        loop.stop()

    def show_alert(self, text=""):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Notice！")
        dlg.setText(text)
        dlg.exec()

