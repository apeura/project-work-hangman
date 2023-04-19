from flask import render_template, Flask, Response, jsonify, abort, make_response, request, json
from frontend.util.utility import sort_score, format_score, read_score, adjust_ids, make_2D_array

app = Flask(__name__)

scores_str = read_score()

#Allow origins
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route("/") # index? see below
def root():
    return "<h1>hello, this is the root location for highscores</h1>"

#Get all scores DONE!
@app.route("/scores")
def get_scores():
    return make_response(scores_str, 200)

#Get a single score based on the id DONE!
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
@app.route("/scores/")
def get_asc_or_desc_scores(order_score):
    #all_scores_sorted = sort_score()
    #i = 0
    w#hile i > order
    #return make_response(scores_str, 200)
    pass

#Fetching all scores with limit DONE!
@app.route("/scores/limit/<int:limit>")
def get_scores_limit(limit):

    all_scores_sorted = sort_score()
    print(all_scores_sorted)
    scores_within_limit = []

    if limit > len(all_scores_sorted):
        return abort(404)

    i = 0
    while i < limit:
        scores_within_limit.append(all_scores_sorted[i])
        i += 1

    return make_response(scores_within_limit, 200)

#Delete a score DONE!
@app.route('/scores/<int:the_id>', methods=['DELETE'])
def delete_score(the_id):
    if the_id < 0:
        return abort(404)

    scores_s = json.loads(read_score())
    print(scores_s)

    try:
        print(scores_s["scores"][the_id-1]) # {'id': 1, 'time': '00.00.01', 'name': 'Leevi'}
        del scores_s["scores"][the_id-1]
        adjust_ids(scores_s, the_id)

        return make_response("Score removed succesfully!", 204)
    except:

        return abort(404, description= "Score not found")

#adding a score DONE! But testing?
@app.route('/scores', methods=['POST'])
def add_highscore():
    # load given string and turn in into dictionary
    user_data = json.loads(request.data)
    scores_str.append(user_data)

    return make_response("Score added succesfully!", 209)

@app.route('/kakka', methods = ['GET'])
def index():
    #2D array
    scores_list = make_2D_array()
    scores_string = ""
    i = 0
    while i < len(scores_list):
    #for score in scores_list:
        time = str(scores_list[i][0])
        name = str(scores_list[i][1])
        scores_string += (f'{time}, {name}\n')
        i = i + 1

<<<<<<< HEAD
    return render_template('index.html', names=table_data)
=======
    print (scores_string)
    #table_data = [row.split(',') for row in rows]
>>>>>>> 9215bffdeabbae14bc2500417e72d31170d27664

    #return render_template('form.html', name=name, lname=lname)
    return make_response("nice!", 209)

if __name__ == "__main__":
    app.run(debug=True)