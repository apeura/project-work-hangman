from flask import Flask, jsonify, abort, make_response, json, request

app = Flask(__name__)

#global scores list
scores = [{"id": 1, "time": "1m 20s", "name": "jack"}]


@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route("/scores")
def get_scores():
    return jsonify(scores)


@app.route("/scores")
def get_scores():
    return jsonify(scores)


#goes through scores ('score') in scores list, if id matches the_id returns that score
@app.route('/scores/<int:the_id>')
def get_score(the_id):
    for score in scores:
        if score['id'] == the_id:
            return score
        
    abort(404, description="score not found")


@app.route('/scores/<int:the_id>', methods=['DELETE'])
def delete_score(the_id):
    for score in scores:
        if score['id'] == the_id:
            scores.remove(score)
            return make_response("", 204)
        
    abort(404, description="score not found")


@app.route('/scores', methods=['POST'])
def add_score():
    # load given string and turn in into dictionary
    score = json.loads(request.data)
    for c in scores:
        if c['id'] == score['id']:
            abort(409, description="score ID already exists")
            
    scores.append(score)
    return make_response("", 201)
    
@app.route("/")
def root():
    return "<h1>The scores are visible over at /scores </h1>"

if __name__ == "__main__":
    app.run()
