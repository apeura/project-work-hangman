from flask import Flask, Response, jsonify, abort, make_response, request, json
from frontend.util.utility import format_score, read_score, generate_id

app = Flask(__name__)

scores = format_score()

#Allow origins
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route("/")
def root():
    return "<h1>hello, this is the root location for highscores</h1>"

#Get all scores
@app.route("/scores")
def get_scores():
    my_response = jsonify(scores)
    return make_response(my_response, 200)

#Get a single score based on the id
@app.route('/scores/<int:the_id>')
def get_score(the_id):
    # your implementation
    if the_id < 0:
        return abort(404)
    
    if the_id > len(scores):
        return abort(404)

    score = scores[the_id-1]
    return jsonify(score)

#Returns a descended or ascended order of the score list.
@app.route("/scores")
def get_asc_or_desc_scores(order_score):
    print("moi")


#Fetching all scores with limit
@app.route("/scores")
def get_scores_limit(limit):
    for x in scores:
        pass
    

#Delete a score
@app.route('/scores/<int:the_id>', methods=['DELETE'])
def delete_score(the_id):
    if the_id < 0:
        return abort(404)
    
    for score in scores:
        if score["id"] == the_id:
            scores.remove(score)
            return make_response("Score removed succesfully!", 204)
        
    return abort(404, description= "Score not found")

#saving a score
@app.route('/scores', methods=['POST'])
def save_highscore():
    # load given string and turn in into dictionary
    user_data = json.loads(request.data)

    name = user_data['name']
    time = user_data['time']
    id = generate_id()

    new_score = {"id": id, "time": time, "name": name}
    scores.append(new_score)
    return make_response("Score added succesfully!", 209)

if __name__ == "__main__":
    app.run(debug=True)