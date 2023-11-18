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

hdfs_path="hdfs://hadoop:9900/nifty_data/"

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

@app.route('/get_nifty_five_minute_data', methods=['GET'])
def get_five_minute_data():
    df = pd.read_csv(relpath('dataset/NIFTY_5_min_ISO.csv'))
    data = df.loc[0]
    df.drop(index=df.iloc[0].name, inplace=True)
    df.to_csv(relpath('dataset/NIFTY_5_min_ISO.csv'), index=False)
    result = {
        'date': data['time'],
        'open': data['open'],
        'close': data['close'],
        'high': data['high'],
        'low': data['low'],
        'volume': data['volume']
    }
    
    result = json.dumps(result, cls=NpEncoder)

    return jsonify(result)

@app.route('/get_nifty_fifteen_minute_data', methods=['GET'])
def get_fifteen_minute_data():
    df = pd.read_csv(relpath('dataset/NIFTY_15_min_ISO.csv'))
    data = df.loc[0]
    df.drop(index=df.iloc[0].name, inplace=True)
    df.to_csv(relpath('dataset/NIFTY_15_min_ISO.csv'), index=False)
    result = {
        'date': data['time'],
        'open': data['open'],
        'close': data['close'],
        'high': data['high'],
        'low': data['low'],
        'volume': data['volume']
    }
    
    result = json.dumps(result, cls=NpEncoder)

    return jsonify(result)

@app.route('/get_nifty_one_hour_data', methods=['GET'])
def get_one_hour_data():
    df = pd.read_csv(relpath('dataset/NIFTY_1_hr_ISO.csv'))
    data = df.loc[0]
    df.drop(index=df.iloc[0].name, inplace=True)
    df.to_csv(relpath('dataset/NIFTY_1_hr_ISO.csv'), index=False)
    result = {
        'date': data['time'],
        'open': data['open'],
        'close': data['close'],
        'high': data['high'],
        'low': data['low'],
        'volume': data['volume']
    }
    
    result = json.dumps(result, cls=NpEncoder)

    return jsonify(result)

@app.route('/get_nifty_one_day_data', methods=['GET'])
def get_one_day_data():
    df = pd.read_csv(relpath('dataset/NIFTY_1_day_ISO.csv'))
    data = df.loc[0]
    df.drop(index=df.iloc[0].name, inplace=True)
    df.to_csv(relpath('dataset/NIFTY_1_day_ISO.csv'), index=False)
    result = {
        'date': data['time'],
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

timeMap = {
    "1_min": "nifty.csv",
    "5_min": "five_min.csv",
    "15_min": "fifteen_min.csv",
    "1_hr": "one_hour.csv",
    "1_day": "one_day.csv"
}

@app.route('/batch/niftyData/<timeframe>/<qty>', methods=['GET'])
def get_csv_data(timeframe, qty):
    try:
        with hdfs.open(hdfs_path+timeMap[timeframe], 'r') as f:
            if timeframe == '1_min':
                df = pd.read_csv(f)
            else:
                df = pd.read_csv(f, names=['date', 'open', 'close', 'low', 'high', 'volume'])

            df = df.tail(int(qty))
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
                    "MFI": row['MFI'],
                    'volume': row['volume']
                })
            
            f.close()
            return jsonify(data)

    except Exception as e:
        print(str(e))
        return str(e), 500

if __name__ == '__main__':
    app.run(port=4000, debug=True, use_reloader=False)