from kafka import KafkaProducer
from json import dumps
from apscheduler.schedulers.background import BackgroundScheduler
import time
import requests
import json

producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'], 
    api_version=(0,11,5), 
    value_serializer=lambda K: dumps(K).encode('utf-8')
    )
scheduler = BackgroundScheduler()

def get_1_min_from_api():
    try:
        res = requests.get('http://127.0.0.1:4000/get_nifty_minute_data')
        res = json.loads(res.json())
        res['timeframe'] = '1_min'
        producer.send('StockStream', dumps(res))
        print(res)
    except Exception as e:
        print(e)

def get_5_min_from_api():
    try:
        res = requests.get('http://127.0.0.1:4000/get_nifty_five_minute_data')
        res = json.loads(res.json())
        res['timeframe'] = '5_min'
        producer.send('StockStream', dumps(res))
        print(res)
    except Exception as e:
        print(e)

def get_15_min_from_api():
    try:
        res = requests.get('http://127.0.0.1:4000/get_nifty_fifteen_minute_data')
        res = json.loads(res.json())
        res['timeframe'] = '15_min'
        producer.send('StockStream', dumps(res))
        print(res)
    except Exception as e:
        print(e)

def get_1_hr_from_api():
    try:
        res = requests.get('http://127.0.0.1:4000/get_nifty_one_hour_data')
        res = json.loads(res.json())
        res['timeframe'] = '1_hour'
        producer.send('StockStream', dumps(res))
        print(res)
    except Exception as e:
        print(e)

def get_1_day_from_api():
    try:
        res = requests.get('http://127.0.0.1:4000/get_nifty_one_day_data')
        res = json.loads(res.json())
        res['timeframe'] = '1_day'
        producer.send('StockStream', dumps(res))
        print(res)
    except Exception as e:
        print(e)

scheduler.add_job(get_1_min_from_api, 'interval', seconds=60)
scheduler.add_job(get_5_min_from_api, 'interval', seconds=5)
scheduler.add_job(get_15_min_from_api, 'interval', seconds=10)
scheduler.add_job(get_1_hr_from_api, 'interval', seconds=15)
scheduler.add_job(get_1_day_from_api, 'interval', seconds=20)

if __name__ == "__main__":
    scheduler.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('Producer stopped!')
        producer.flush()
        producer.close()
        scheduler.shutdown()