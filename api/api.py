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
    proxies_list = load.load(num, type='good')

    for proxy in proxies_list:
        proxies = {
            'http': f'socks5://{proxy}',
            'https': f'socks5://{proxy}'
        }
        try:
            response = requests.get('https://httpbin.org/ip', proxies=proxies, timeout=10)
            response.raise_for_status() 
            
            if response.status_code == 200:
                ip_info = ip_lookup.get_ip_info(proxy.split(':')[0])
                return jsonify({
                    'ip': ip_info.get('ip'),
                    'country': ip_info.get('country'),
                    'cc': ip_info.get('country_code'),
                    'port': proxy.split(':')[1]
                })
        
        except requests.RequestException:
            load.remove(proxy_type='good', which=proxy)
            continue  

    return jsonify({'error': 'No valid proxy available'}), 500


if __name__ == '__main__':
    app.run(debug=True)