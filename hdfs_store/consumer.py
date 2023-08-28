from kafka import KafkaConsumer
import json
import pydoop.hdfs as hdfs

consumer = KafkaConsumer(
    'MajorProject', 
    bootstrap_servers=['localhost:9092'], 
    auto_offset_reset='latest',
    enable_auto_commit=True,
    value_deserializer=lambda K: json.loads(K.decode('utf-8'))
    )

hdfs_path="hdfs://hadoop:9000/nifty_data/nifty.csv"

if __name__ == "__main__":
    try:
        for data in consumer:
            json_data = json.loads(data.value)
            json_data = json.loads(json_data)
            csv_string = f"{json_data['date']}, {json_data['open']}, {json_data['close']}, {json_data['low']}, {json_data['high']}, {json_data['volume']}"
            with hdfs.open(hdfs_path, 'at') as f:
                f.write(f'{csv_string} \n')

    except KeyboardInterrupt:
        print('Consumer closed!')