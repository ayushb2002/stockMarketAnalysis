from apscheduler.schedulers.background import BackgroundScheduler
import time
import requests

scheduler = BackgroundScheduler()

def get_data_from_api():
    res = requests.get('http://127.0.0.1:4000/get_minute_data')
    res = res.json()
    print(res)

scheduler.add_job(get_data_from_api, 'interval', seconds=60)

if __name__ == "__main__":
    scheduler.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('Script stopped!')

    scheduler.shutdown()

