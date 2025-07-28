from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "✅ MCP server is running", 200

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    return jsonify({"status": "success", "received": data})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
