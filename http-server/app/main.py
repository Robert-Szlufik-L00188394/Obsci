
from flask import Flask, jsonify
from generator import generate_metrics

app = Flask(__name__)

@app.route("/metrics", methods=["GET"])
def metrics():
    return jsonify(generate_metrics())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
