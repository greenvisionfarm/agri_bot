import datetime
import schedule
import time

from data_core.get_data import request_ema, request_ebm, request_eco


def update_data():
    request_ema(), request_ebm(), request_eco()
    print(f'Date was update at{datetime.datetime.now()}')


# schedule.every().day.at("18:30").do(update_data)
schedule.every(1).minutes.do(update_data)

while True:
    schedule.run_pending()
    time.sleep(5)
