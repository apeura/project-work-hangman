from flask import Flask, Response, jsonify, abort, make_response, request, json
from frontend.util.utility import sort_score, format_score, read_score, adjust_ids

app = Flask(__name__)

scores = read_score()

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
    sort_score()
    pass


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
            scores.pop(score)
            adjust_ids(the_id)
            return make_response("Score removed succesfully!", 204)
        
    return abort(404, description= "Score not found")

#adding a score
@app.route('/scores', methods=['POST'])
def add_highscore():
    # load given string and turn in into dictionary
    user_data = json.loads(request.data)
    scores.append(user_data)

   # id = user_data['id']
   # name = user_data['name']
    #time = user_data['time']
    #save_to_score(id, time, name)
    
    #return make_response("", 201)

    #1
    #new_score = {"id": id, "time": time, "name": name}
    #print(new_score)

    #2
    #scores["id"].append(id)
    #scores["time"].append(time)
    #scores["name"].append(name)

    return make_response("Score added succesfully!", 209)

if __name__ == "__main__":
    app.run(debug=True)