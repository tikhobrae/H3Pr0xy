from flask import Flask, jsonify, request
import time
import load

app = Flask('H3Pr0xy')
app = Flask(__name__.split('.')[0])


@app.route('/', methods=['GET'])
def hello():
    return "Welcome, to H3Pr0xy!"


@app.route('/time', methods=['GET'])
def get_time():
    return jsonify(time.ctime())


@app.route('/avl')
def get_proxy():
    num = request.args.get('num', default=1, type=int)  
    
    proxy = load.load(num)


    return jsonify('proxy', proxy)

if __name__ == '__main__':
    app.run(debug=True)