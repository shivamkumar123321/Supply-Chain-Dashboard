from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "✅ MCP proxy running", 200

@app.route("/search", methods=["GET"])
def search_get():
    return "Use POST to /search with JSON payload", 200

@app.route("/search", methods=["POST"])
def translate_and_search():
    data = request.json
    # … your translation + Algolia proxy logic …
    return jsonify({"status": "success", "received": data})

if __name__ == "__main__":
    # This line actually starts the server on port 5000
    app.run(host="0.0.0.0", port=5000, debug=True)


