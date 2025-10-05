from flask import Flask, jsonify, send_from_directory
from pathlib import Path
import orjson as json

app = Flask(__name__)

# Serve the dashboard HTML
@app.route("/")
def dashboard():
    return send_from_directory(".", "dashboard.html")

# API endpoint to fetch scored data
@app.route("/data")
def get_data():
    scored_file = Path("data/scored/all_scored.jsonl")  # Adjust path if needed
    all_data = []

    if not scored_file.exists():
        return jsonify({"error": "Scored data file not found. Run the pipeline first."}), 404

    with open(scored_file, "rb") as f:
        for line in f:
            all_data.append(json.loads(line))

    return jsonify(all_data)

if __name__ == "__main__":
    app.run(debug=True)