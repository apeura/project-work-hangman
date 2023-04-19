from flask import render_template, Flask, Response, jsonify, abort, make_response, request, json
from frontend.util.utility import sort_score, format_score, read_score, adjust_ids

app = Flask(__name__)

scores_str = read_score()

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
    return make_response(scores_str, 200)

#Get a single score based on the id
@app.route('/scores/<int:the_id>')
def get_score(the_id):

    #dict version of scores
    scores_s = json.loads(scores_str)
    #go through scores, if id match return that
    for s in scores_s["scores"]:  
        if s["id"] == the_id: 
            return s

    abort(404, description="Score not found")

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

    scores_s = json.loads(read_score())

    try:
        print(scores_s["scores"][the_id-1]) # {'id': 1, 'time': '00.00.01', 'name': 'Leevi'}
        del scores_s["scores"][the_id-1]
        adjust_ids(scores_s, the_id)

        return make_response("Score removed succesfully!", 204)
    except:

        return abort(404, description= "Score not found")

#adding a score
@app.route('/scores', methods=['POST'])
def add_highscore():
    # load given string and turn in into dictionary
    user_data = json.loads(request.data)
    scores_str.append(user_data)

    return make_response("Score added succesfully!", 209)

@app.route('/scores', methods = ['GET'])
def index():

    scores_dict = json.loads(scores_str)

    #2D array
    rows = scores_dict.split('\n')
    table_data = [row.split(',') for row in rows]

    return render_template('form.html', names=table_data, name=name, lname=lname)


if __name__ == "__main__":
    app.run(debug=True)