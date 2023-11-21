from flask import Flask, jsonify
import pandas as pd
from os.path import relpath
import json
import numpy as np
import pydoop.hdfs as hdfs
from flask_cors import CORS 
import torch
import torch.nn as nn
from sklearn.preprocessing import StandardScaler

class PriceChangePredictorLSTM(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers=1):
        super(PriceChangePredictorLSTM, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :])
        return out
    
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

modelMap = {
    "5_min": "model/5_min_final.pth",
    "15_min": "model/15_min_final.pth",
    "1_hr": "model/1_hour_final.pth",
    "1_day": "model/1_day_final.pth"
}

def getWRMIndicator(timeframe, data):
    scaler = StandardScaler()

    if isinstance(data, pd.Series):
        data = pd.DataFrame([data])

    data[['RSI', 'MACD']] = scaler.fit_transform(data[['RSI', 'MACD']])
    data_tensor = torch.tensor(data[['RSI', 'MACD']].values, dtype=torch.float32)

    input_size = 2
    hidden_size = 64
    num_layers = 2 if timeframe == '5_min' else 4
    loaded_model = PriceChangePredictorLSTM(input_size, hidden_size, num_layers)
    loaded_model.load_state_dict(torch.load(modelMap[timeframe]))
    loaded_model.eval()

    with torch.no_grad():
        predictions = loaded_model(data_tensor.unsqueeze(1))

    print(predictions.item())
    return predictions.item()

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
        'volume': data['volume'],
        'RSI': data['RSI'],
        'MACD': data['MACD'],
        "WRM": 0
    }
    
    result = json.dumps(result, cls=NpEncoder)

    return jsonify(result)

@app.route('/get_nifty_five_minute_data', methods=['GET'])
def get_five_minute_data():
    df = pd.read_csv(relpath('dataset/NIFTY_5_min_ISO.csv'))
    data = df.loc[0]
    df.drop(index=df.iloc[0].name, inplace=True)
    df.to_csv(relpath('dataset/NIFTY_5_min_ISO.csv'), index=False)
    data['WRM'] = getWRMIndicator('5_min', data)
    result = {
        'date': data['time'],
        'open': data['open'],
        'close': data['close'],
        'high': data['high'],
        'low': data['low'],
        'volume': data['volume'],
        'RSI': data['RSI'],
        'MACD': data['MACD'],
        'WRM': data['WRM']
    }

    result = json.dumps(result, cls=NpEncoder)

    return jsonify(result)

@app.route('/get_nifty_fifteen_minute_data', methods=['GET'])
def get_fifteen_minute_data():
    df = pd.read_csv(relpath('dataset/NIFTY_15_min_ISO.csv'))
    data = df.loc[0]
    df.drop(index=df.iloc[0].name, inplace=True)
    df.to_csv(relpath('dataset/NIFTY_15_min_ISO.csv'), index=False)
    data['WRM'] = getWRMIndicator('15_min', data)
    result = {
        'date': data['time'],
        'open': data['open'],
        'close': data['close'],
        'high': data['high'],
        'low': data['low'],
        'volume': data['volume'],
        'RSI': data['RSI'],
        'MACD': data['MACD'],
        'WRM': data['WRM']
    }
    
    result = json.dumps(result, cls=NpEncoder)

    return jsonify(result)

@app.route('/get_nifty_one_hour_data', methods=['GET'])
def get_one_hour_data():
    df = pd.read_csv(relpath('dataset/NIFTY_1_hr_ISO.csv'))
    data = df.loc[0]
    df.drop(index=df.iloc[0].name, inplace=True)
    df.to_csv(relpath('dataset/NIFTY_1_hr_ISO.csv'), index=False)
    data['WRM'] = getWRMIndicator('1_hr', data)
    result = {
        'date': data['time'],
        'open': data['open'],
        'close': data['close'],
        'high': data['high'],
        'low': data['low'],
        'volume': data['volume'],
        'RSI': data['RSI'],
        'MACD': data['MACD'],
        'WRM': data['WRM']
    }
    
    result = json.dumps(result, cls=NpEncoder)

    return jsonify(result)

@app.route('/get_nifty_one_day_data', methods=['GET'])
def get_one_day_data():
    df = pd.read_csv(relpath('dataset/NIFTY_1_day_ISO.csv'))
    data = df.loc[0]
    df.drop(index=df.iloc[0].name, inplace=True)
    df.to_csv(relpath('dataset/NIFTY_1_day_ISO.csv'), index=False)
    data['WRM'] = getWRMIndicator('1_day', data)
    result = {
        'date': data['time'],
        'open': data['open'],
        'close': data['close'],
        'high': data['high'],
        'low': data['low'],
        'volume': data['volume'],
        'RSI': data['RSI'],
        'MACD': data['MACD'],
        'WRM': data['WRM']
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
    if timeframe != '1_min':
        input_size = 2
        hidden_size = 64
        if timeframe == '5_min': 
            num_layers = 2 
        else:
            num_layers = 4
        loaded_model = PriceChangePredictorLSTM(input_size, hidden_size, num_layers)
        loaded_model.load_state_dict(torch.load(modelMap[timeframe]))
        loaded_model.eval()
        scaler = StandardScaler()

    try:
        with hdfs.open(hdfs_path+timeMap[timeframe], 'r') as f:
            df = pd.read_csv(f)
            df = df.tail(int(qty))
            df['SMA'] = calculate_sma(df)
            df['MFI'] = calculate_mfi(df)

            if timeframe != '1_min':
                df[['RSI', 'MACD']] = scaler.fit_transform(df[['RSI', 'MACD']])
                data_tensor = torch.tensor(df[['RSI', 'MACD']].values, dtype=torch.float32)
                with torch.no_grad():
                    predictions = loaded_model(data_tensor.unsqueeze(1))
                
                df['WRM'] = predictions.view(-1).numpy()

            data = []
            for _, row in df.iterrows():
                if timeframe != "1_min":
                    data.append({
                        "x": row['date'],  
                        "y": [row['open'], row['high'], row['low'], row['close']],
                        "RSI": row['RSI'],
                        "SMA": row['SMA'],
                        "MFI": row['MFI'],
                        "MACD": row['MACD'],
                        'volume': row['volume'],
                        "WRM": row['WRM']
                    })
                else:
                    data.append({
                        "x": row['date'],  
                        "y": [row['open'], row['high'], row['low'], row['close']],
                        "RSI": row['RSI'],
                        "SMA": row['SMA'],
                        "MFI": row['MFI'],
                        "MACD": row['MACD'],
                        'volume': row['volume'],
                    })
            
            f.close()
            return jsonify(data)

    except Exception as e:
        print(str(e))
        return str(e), 500

if __name__ == '__main__':
    app.run(port=4000, debug=True, use_reloader=False)