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
STREAM_INDEX = 0
df = pd.read_csv(relpath('dataset/stream.csv'))

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message":"Up and runnning"})

@app.route('/get_minute_data', methods=['GET'])
def get_minute_data():
    global STREAM_INDEX
    data = df.loc[STREAM_INDEX,:]
    STREAM_INDEX += 1
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