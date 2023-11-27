from kafka import KafkaConsumer
import json
import pydoop.hdfs as hdfs

consumer = KafkaConsumer(
    'NiftyStream', 
    bootstrap_servers=['kafka:9092'], 
    auto_offset_reset='latest',
    enable_auto_commit=True,
    value_deserializer=lambda K: json.loads(K.decode('utf-8'))
    )

hdfs_path = {
        "1_min": "hdfs://hadoop:9900/nifty_data/nifty.csv", 
        "5_min": "hdfs://hadoop:9900/nifty_data/five_min.csv", 
        "15_min": "hdfs://hadoop:9900/nifty_data/fifteen_min.csv",
        "1_hour": "hdfs://hadoop:9900/nifty_data/one_hour.csv",
        "1_day": "hdfs://hadoop:9900/nifty_data/one_day.csv"
    }

if __name__ == "__main__":
    try:
        for data in consumer:
            json_data = json.loads(data.value)
            csv_string = f"{json_data['date']}, {json_data['open']}, {json_data['close']}, {json_data['low']}, {json_data['high']}, {json_data['volume']}, {json_data['RSI']}, {json_data['MACD']}"
            with hdfs.open(hdfs_path[json_data['timeframe']], 'at') as f:
                print('Record received, writing to hdfs...')
                f.write(f'{csv_string} \n')
                f.close()

    except KeyboardInterrupt:
        print('Consumer closed!')