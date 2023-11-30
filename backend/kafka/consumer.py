from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'StockStream', 
    bootstrap_servers=['kafka:9092'], 
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id=None,
    value_deserializer=lambda K: json.loads(K.decode('utf-8'))
    )

if __name__ == "__main__":
    try:
        for data in consumer:
            json_data = json.loads(data.value)
            # json_data = json.loads(json_data)
            print(json_data)
    except KeyboardInterrupt:
        print('Consumer closed!')