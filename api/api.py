from flask import Flask, jsonify, request
import time
import load
import requests
from ip_lookup import IPLookup

ip_lookup = IPLookup()

app = Flask('H3Pr0xy')
app = Flask(__name__.split('.')[0])


@app.route('/', methods=['GET'])
def hello():
    return "Welcome, to H3Pr0xy!"


@app.route('/time', methods=['GET'])
def get_time():
    return jsonify(time.ctime())


@app.route('/getproxy')
def get_proxy():
    num = request.args.get('num', default=20, type=int)  
    proxy = load.load(num, type='all')
    return jsonify({'proxy': proxy})

@app.route('/good', methods=['GET'])
def get_good():
    num = request.args.get('num', default=1, type=int)
    proxy = load.load(num, type='good')
    ip_info = ip_lookup.get_ip_info(proxy[0].split(':')[0])
    
    try:
        return jsonify({
            'ip': ip_info.get('ip'),
            'country': ip_info.get('country'),
            'cc': ip_info.get('country_code'),
            'port': proxy[0].split(':')[1]
        })
    except:
        return jsonify({'error': 'Eroooor'})
    
    # proxies = {
    #     'http': f'socks5://{proxy[0]}',
    #     'https': f'socks5://{proxy[0]}'
    # }

    # try:
    #     response = requests.get('https://ipinfo.io/json', proxies=proxies, timeout=8)
    #     response.raise_for_status() 
        
    #     data = response.json()
    #     return jsonify({
    #         'ip': data.get('ip'),
    #         'country': data.get('city'),
    #         'region': data.get('region'),
    #         'cc': data.get('country'),
    #         'port': proxy[0].split(':')[1]
    #     })

    # except requests.RequestException as e:
    #     return jsonify({'error': str(e)}, {'ip': proxy}), 500


if __name__ == '__main__':
    app.run(debug=True)