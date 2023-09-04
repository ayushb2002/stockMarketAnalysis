from flask import Flask, jsonify, request
import pandas as pd
from os.path import relpath
import json
import numpy as np

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(port=4000, debug=True, use_reloader=False)