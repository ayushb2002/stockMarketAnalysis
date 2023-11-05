from kafka import KafkaProducer
from json import dumps
from apscheduler.schedulers.background import BackgroundScheduler
import time
import requests

producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'], 
    api_version=(0,11,5), 
    value_serializer=lambda K: dumps(K).encode('utf-8')
    )
scheduler = BackgroundScheduler()

def get_data_from_api():
    try:
        res = requests.get('http://127.0.0.1:4000/get_nifty_minute_data')
        res = res.json()
        producer.send('StockStream', dumps(res))
        print(res)
    except Exception as e:
        print(e)

scheduler.add_job(get_data_from_api, 'interval', seconds=30)

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