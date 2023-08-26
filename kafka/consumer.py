from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'MajorProject', 
    bootstrap_servers=['localhost:9092'], 
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda K: json.loads(K.decode('utf-8'))
    )

if __name__ == "__main__":
    try:
        for data in consumer:
            json_data = json.loads(data.value)
            print(json_data)
    except KeyboardInterrupt:
        print('Consumer closed!')