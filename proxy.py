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
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f0f0f0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            width: 400px;
            padding: 40px;
            background: #fff;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        h1 {
            color: #333;
            margin-bottom: 30px;
        }
        form {
            margin-top: 20px;
        }
        label {
            font-weight: bold;
            display: block;
            margin-bottom: 10px;
            color: #555;
            text-align: left;
        }
        input[type="text"] {
            width: calc(100% - 24px);
            padding: 12px;
            margin-bottom: 20px;
            border: 1px solid #ddd;
            border-radius: 5px;
            box-sizing: border-box;
            font-size: 16px;
            outline: none;
            transition: border-color 0.3s;
        }
        input[type="text"]:focus {
            border-color: #4CAF50;
        }
        input[type="submit"] {
            background-color: #4CAF50;
            color: white;
            padding: 14px 0;
            width: 100%;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 18px;
            transition: background-color 0.3s;
        }
        input[type="submit"]:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Proxy Interface</h1>
        <form action="/proxy" method="post">
            <label for="url">Enter URL:</label><br>
            <input type="text" id="url" name="url" placeholder="https://example.com" required><br>
            <input type="submit" value="Submit">
        </form>
    </div>
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
