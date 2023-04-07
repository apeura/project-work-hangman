from flask import Flask, Response, jsonify, abort, make_response, request, json
from frontend.util.utility import save_to_score, generate_id
app = Flask(__name__)

scores = [{'id': 1, 'name': 'moi', 'time': '1m 2s'}]

#Get all scores
@app.route("/scores")
def get_scores():
    return jsonify(scores)

if __name__ == "__main__":
    app.run()