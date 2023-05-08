import schedule
import time
from Singleton import *
import datetime
import datetime


class ScheduleHelper:
    type_place_order = "place_order"
    type_check_order = "check_order"
    type_close_order = 'close_order'
    type_check_close_rate = "type_check_close_by_rate"

    @staticmethod
    def cancel_all():
        schedule.clear()

    @staticmethod
    def schedule_job_at(block, time, tag: str = type_place_order):
        schedule.every().day.at(time).do(block).tag(tag)

    @staticmethod
    def schedule_repeat_until(block, secs: int = 5, tag: str = type_check_order, count: int = 6):
        schedule.every(secs).seconds.until(datetime.timedelta(seconds=secs*count)).do(block).tag(tag)

    @staticmethod
    def schedule_repeat_forever(block, secs: int = 5, tag: str = type_check_close_rate):
        schedule.every(secs).seconds.do(block).tag(tag)
    @staticmethod
    def check_pending():
        schedule.run_pending()

    @staticmethod
    def get_place_order_jobs(ty: str = type_place_order):
        return schedule.get_jobs(ty)

