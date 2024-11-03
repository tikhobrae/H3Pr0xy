from flask import Flask, jsonify, request
import time
import load  # Assuming load is a module responsible for proxy handling
import requests
from ip_lookup import IPLookup  # Custom module for IP lookup functionality

# Initialize the IPLookup instance
ip_lookup = IPLookup()

# Create a new Flask application named 'H3Pr0xy'
app = Flask('H3Pr0xy')
app = Flask(__name__.split('.')[0])  # Additional initialization, might not be necessary

# Define the root route that returns a welcome message
@app.route('/', methods=['GET'])
def hello():
    return "Welcome, to H3Pr0xy!"  # Returns a simple welcome message

# Define a route to get the current server time
@app.route('/time', methods=['GET'])
def get_time():
    return jsonify(time.ctime())  # Returns the current time in JSON format

# Define a route to get a list of proxies
@app.route('/getproxy')
def get_proxy():
    # Get the number of proxies requested from query parameters, default is 20
    num = request.args.get('num', default=20, type=int)  
    proxy = load.load(num, type='all')  # Load proxies of type 'all'
    return jsonify({'proxy': proxy})  # Return the proxies in JSON format

# Define a route to check for valid proxies
@app.route('/good', methods=['GET'])
def get_good():
    num = request.args.get('num', default=3, type=int)  # Get the number of good proxies requested, default is 3
    proxies_list = load.load(num, type='good')  # Load good proxies

    # Iterate through the list of proxies
    for proxy in proxies_list:
        # Define the proxy configuration for requests
        proxies = {
            'http': f'socks5://{proxy}',  # Use SOCKS5 for HTTP
            'https': f'socks5://{proxy}'  # Use SOCKS5 for HTTPS
        }
        try:
            # Make a request to httpbin to check if the proxy is valid
            response = requests.get('https://httpbin.org/ip', proxies=proxies, timeout=5)
            response.raise_for_status()  # Raise an error for bad responses
            
            if response.status_code == 200:  # Check if the response is successful
                # Get IP information from the IPLookup instance
                ip_info = ip_lookup.get_ip_info(proxy.split(':')[0])  
                return jsonify({
                    'ip': ip_info.get('ip'),  # Return the IP address
                    'country': ip_info.get('country'),  # Return the country
                    'cc': ip_info.get('country_code'),  # Return the country code
                    'port': proxy.split(':')[1]  # Return the port number
                })
        except requests.RequestException:
            load.remove(proxy_type='good', which=proxy)  # Remove the proxy if it fails
            continue  # Continue to the next proxy in the list

    return jsonify({'error': 'No valid proxy available'}), 500  # Return an error if no valid proxies were found

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)  # Start the server on port 8080
