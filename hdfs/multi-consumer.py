from concurrent.futures import ThreadPoolExecutor
from kafka import KafkaConsumer
import json
import pydoop.hdfs as hdfs
import signal
import sys

def consume_and_store_to_hdfs(topic, hdfs_path):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=['kafka:9092'],
        auto_offset_reset='latest',
        enable_auto_commit=True,
        value_deserializer=lambda K: json.loads(K.decode('utf-8'))
    )

    try:
        for data in consumer:
            json_data = json.loads(data.value)
            json_data = json.loads(json_data)
            csv_string = f"{json_data['date']}, {json_data['open']}, {json_data['close']}, {json_data['low']}, {json_data['high']}, {json_data['volume']}"
            with hdfs.open(hdfs_path, 'at') as f:
                print(f'Record received from {topic}, writing to hdfs...')
                f.write(f'{csv_string}\n')
    except KeyboardInterrupt:
        print(f'Consumer for topic {topic} closed!')
    finally:
        consumer.close()

def exit_handler(signum, frame):
    print("Exiting...")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit_handler)
    print("Cosumer has started!")
    topics = ['OneMinStream', 'FiveMinStream', 'FifteenMinStream', 'OneHrStream', 'OneDayStream']
    hdfs_path = [
        "hdfs://hadoop:9900/nifty_data/nifty.csv", 
        "hdfs://hadoop:9900/nifty_data/five_min.csv", 
        "hdfs://hadoop:9900/nifty_data/fifteen_min.csv",
        "hdfs://hadoop:9900/nifty_data/one_hour.csv",
        "hdfs://hadoop:9900/nifty_data/one_day.csv"
        ]
    
    with ThreadPoolExecutor(max_workers=len(topics)) as executor:
        futures = []
        i = 0
        for topic in topics:
            futures.append(executor.submit(consume_and_store_to_hdfs, topic, hdfs_path[i]))
            i += 1

        for future in futures:
            future.result()
