from flask import Flask, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
scheduler = BackgroundScheduler()

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message":"Up and runnning"})

i = 0

def increment():
    global i
    i += 1
    print(i)    

scheduler.add_job(increment, 'interval', seconds=3)

if __name__ == '__main__':
    scheduler.start()
    app.run(port=4000, debug=True, use_reloader=False)
    scheduler.shutdown()