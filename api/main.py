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

@app.route('/batch/niftyData/<param>', methods=['GET'])
def get_csv_data(param):
    try:
        with hdfs.open(hdfs_path, 'r') as f:
            df = pd.read_csv(f)
            
            data = []
            param = int(param)
            for _, row in df[:param].iterrows():
                data.append({
                    "x": row['date'],  # Assuming 'date' is the column name in your CSV
                    "y": [row['open'], row['high'], row['low'], row['close']]
                })
            
            f.close()
            return jsonify(data)

    except Exception as e:
        print(str(e))
        return str(e), 500

if __name__ == '__main__':
    app.run(port=4000, debug=True, use_reloader=False)