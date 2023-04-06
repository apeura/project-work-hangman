
from flask import Flask, Response, jsonify, abort, make_response, request, json
from frontend.util import get_id
app = Flask(__name__)

scores = [{"id": 1, "time": "1m 20s", "name": "jack"}]

#Get all scores
@app.route("/scores")
def get_scores():
    return jsonify(scores)

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
            print("moi")


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



#Add a score
@app.route('/scores', methods=['POST'])
def add_score():
    # load given string and turn in into dictionary
    #score = json.loads(request.data)

    all_ids = get_id()
    
    for id in all_ids:
        if id["id"] == score["id"]:
            abort(409, description= "Score already excists!")
    
    scores.append(score)
    return make_response("Score added succesfully!", 209)

    #Id generation copied from exercise 8
    generated_id = int(1000000 * random.random())
    for i in range(0, len(customers)):
        if customers[i]['id'] == generated_id:
            return make_response(jsonify("Error: id already exists"), 409)
    save_to_database(customer_name, str(generated_id))
    return make_response("", 201)

# ids always based on how many lines are in scores.txt 
# iteration through current ids, if gap e.g. 1, 2, 4 ... it uses 3 

#Allow origins
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

if __name__ == "__main__":
    app.run()

    