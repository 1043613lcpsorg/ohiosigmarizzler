# proxy.py

from flask import Flask, render_template, request, jsonify
import requests
import argparse

app = Flask(__name__)

# HTML form for input
html_form = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Proxy Interface</title>
</head>
<body>
    <h1>Proxy Interface</h1>
    <h1>Made By Ayaan Khan (1043613lcpsorg) IN DEVELOPMENT MAY NOT WORK CORRECTLY<h1>
    <form action="/proxy" method="post">
        <label for="url">Enter URL:</label><br>
        <input type="text" id="url" name="url" style="width: 300px;"><br><br>
        <input type="submit" value="Submit">
    </form>
</body>
</html>
"""

# Define a function to proxy requests to the desired URL
def proxy_request(url):
    response = requests.get(url)
    return response.content, response.status_code

# Define route for the proxy UI
@app.route('/', methods=['GET'])
def proxy_ui():
    return html_form

# Define route to handle proxy requests
@app.route('/proxy', methods=['POST'])
def proxy():
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'URL not provided'}), 400

    try:
        response_data, status_code = proxy_request(url)
        return response_data, status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def main():
    parser = argparse.ArgumentParser(description="Run a simple proxy server with a user interface.")
    parser.add_argument("--host", default="127.0.0.1", help="Host IP address to run the server on.")
    parser.add_argument("--port", default=5000, type=int, help="Port number to run the server on.")
    args = parser.parse_args()

    app.run(host=args.host, port=args.port, debug=True)

if __name__ == '__main__':
    main()
