from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'MajorProject', 
    bootstrap_servers=['localhost:9092'], 
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda K: json.loads(K.decode('utf-8'))
    )
