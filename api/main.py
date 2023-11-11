from flask import Flask, jsonify
import pandas as pd
from os.path import relpath
import json
import numpy as np
import pydoop.hdfs as hdfs
from flask_cors import CORS 

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

hdfs_path="hdfs://hadoop:9000/nifty_data/nifty.csv"

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message":"Up and runnning"})

@app.route('/get_nifty_minute_data', methods=['GET'])
def get_minute_data():
    df = pd.read_csv(relpath('dataset/stream.csv'))
    data = df.loc[0]
    df.drop(index=df.iloc[0].name, inplace=True)
    df.to_csv(relpath('dataset/stream.csv'), index=False)
    result = {
        'date': data['date'],
        'open': data['open'],
        'close': data['close'],
        'high': data['high'],
        'low': data['low'],
        'volume': data['volume']
    }
    
    result = json.dumps(result, cls=NpEncoder)

    return jsonify(result)

def calculate_rsi(data, window=14):
    delta = data['close'].diff(1)

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))
    rsi = rsi.fillna(0).round(2)
    return rsi

def calculate_sma(data, window=20):
    sma = data['close'].rolling(window=window, min_periods=1).mean()
    sma = sma.fillna(0).round(2)
    return sma

def calculate_mfi(data, window=14):
    typical_price = (data['high'] + data['low'] + data['close']) / 3
    raw_money_flow = typical_price * data['volume']
    money_flow_direction = (typical_price.diff(1) > 0).astype(int)
    positive_money_flow = money_flow_direction * raw_money_flow
    negative_money_flow = -(-money_flow_direction + 1) * raw_money_flow
    positive_money_flow_sum = positive_money_flow.rolling(window=window, min_periods=1).sum()
    negative_money_flow_sum = negative_money_flow.rolling(window=window, min_periods=1).sum()
    money_flow_ratio = positive_money_flow_sum / negative_money_flow_sum
    mfi = 100 - (100 / (1 + money_flow_ratio))
    mfi = mfi.fillna(0).round(3)
    return mfi

@app.route('/batch/niftyData/<param>', methods=['GET'])
def get_csv_data(param):
    try:
        with hdfs.open(hdfs_path, 'r') as f:
            df = pd.read_csv(f)
            df = df.tail(int(param))
            df['RSI'] = calculate_rsi(df)
            df['SMA'] = calculate_sma(df)
            df['MFI'] = calculate_mfi(df)
            data = []
            for _, row in df.iterrows():
                data.append({
                    "x": row['date'],  
                    "y": [row['open'], row['high'], row['low'], row['close']],
                    "RSI": row['RSI'],
                    "SMA": row['SMA'],
                    "MFI": row['MFI']
                })
            
            f.close()
            return jsonify(data)

    except Exception as e:
        print(str(e))
        return str(e), 500

if __name__ == '__main__':
    app.run(port=4000, debug=True, use_reloader=False)