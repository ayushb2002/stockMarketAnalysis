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

hdfs_path="hdfs://hadoop:9000/nifty_data/nifty_store.json"

if __name__ == "__main__":
    try:
        for data in consumer:
            json_data = json.loads(data.value)
            print(json_data)

            with hdfs.open(hdfs_path, 'at') as f:
                print("Storing in HDFS!")
                f.write(f'{json_data} \n')

    except KeyboardInterrupt:
        print('Consumer closed!')