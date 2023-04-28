from flask import render_template, Flask, jsonify, abort, make_response, request, json
from frontend.util.utility import *
from dotenv import load_dotenv
import os, bcrypt, tempfile, firebase_admin, io
from firebase_admin import credentials, storage

"""
This module contains functions related to Flask and backend operations.
Methods format, add, delete and sort data.
Firebase and API_KEY functionalities are implemented.
"""

app = Flask(__name__)

load_dotenv()

API_KEY = os.environ.get('API_KEY')
json_str = os.environ.get('firebase')

if json_str:
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(json_str)
        temp_path = f.name

    cred = credentials.Certificate(temp_path)

    firebase_admin.initialize_app(cred, {
        'storageBucket': os.environ.get('bucket')
    })

    bucket = storage.bucket()

else:
    raise ValueError("Firebase configuration is not set")


def check_api_key(pw):
    """ Checks the validity of the password that's been sent to backend
    Returns
    -------
        Boolean true or false depending on passwords validity
    """
    # This implementation was resourced from Topias Laatu

    if type(pw) != str:
        raise Exception("Give password as string object")
    
    # hashing the API_KEY that has been turned to bytes array
    # with randomly generated salt
    hash = bcrypt.hashpw(API_KEY.encode('utf-8'), bcrypt.gensalt())

    # checking password received as parameter with api key
    result = bcrypt.checkpw(pw.encode('utf-8'), hash)

    # returned values are boolean type
    return True if result else False

@app.after_request
def after_request(response):
    """
    Sets the Access-Control-Allow-Origin header to allow cross-origin resource sharing for all origins 
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/')
def index():
    """ Formats scores data into rows and table_data that can be used in HTML leaderboard
    Returns
    -------
        Renders template for index.html with scores data 
    """
    scores_list = make_2D_array()
    scores_string = ""

    # If the length of the scores_list is 0, returns "-" to the HTML
    # Making it show empty
    if len(scores_list) == 0:
        return render_template('index.html', scores="-", time="-", name="-")

    i = 0
    while i < len(scores_list):
    #for score in scores_list:
        time = str(scores_list[i][0])
        name = str(scores_list[i][1])
        scores_string += (f'{time}, {name}\n')
        i = i + 1
    
    # Splits each score into rows, which can be shown on their own rows on
    # The HTML site
    rows = scores_string.split('\n')

    table_data = [row.split(',') for row in rows]

    return render_template('index.html', scores=table_data, time=time, name=name)

@app.route("/all_scores")
def get_scores():
    """ Returns all scores dict 
    Returns
    -------
        Returns all score data in dict form or if password is incorrect gives 404
    """
    password = request.args.get('pw')

    blob = bucket.blob('scores.json')
    content = blob.download_as_string().decode('utf-8')
    data = json.loads(content)
    print(data)

    return jsonify(data) if check_api_key(password) else make_response("Incorrect password", 404)

@app.route('/scores/<int:the_id>')
def get_score(the_id):
    """ Returns one score based on id.
    Parameters
    ----------
    Int : `the_id`
        The id the function searches for and returns
    Returns
    -------
        Returns score with matching id, if the_id is not found or password is incorrect gives 404
    """

    password = request.args.get('pw')
    if check_api_key(password):
        blob = bucket.blob('scores.json')
        content = blob.download_as_string().decode('utf-8')
        scores_s = json.loads(content)

        for s in scores_s["scores"]:  
            if s["id"] == the_id: 
                return s

        abort(404, description="Score not found")
    
    else:
        make_response("Incorrect password", 404)

@app.route("/order/<string:order>", methods = ['GET'])
def get_asc_or_desc_scores(order):
    """ Returns scores in ascending or decending order based on 'order' variable.
    Parameters
    ----------
    String : `order`
        Determines if scores are shown in asc or desc order
    Returns
    -------
        Returns scores in desired order, if order is not valid or password is incorrect gives 404
    """

    password = request.args.get('pw')
    if check_api_key(password):
        if order == "asc":
            return make_response(sort_score(False))
        
        if order == "desc":
            return make_response(sort_score(True))

        else:
            return abort(404, description="Order must be 'asc' or 'desc'")
    
    else:
        make_response("Incorrect password", 404)

@app.route("/scores/formatted")
def return_scores_in_format():
    """ Returns scores formatted into string including time and name.
    Returns
    -------
        Returns no scores message if no scores or formatted string of scores. 404 if password incorrect
    """

    password = request.args.get('pw')
    if check_api_key(password):
        scores_in_order_list = make_2D_array()
        top_10_scores = []
        formatted_str = ""

        if len(scores_in_order_list ) == 0:
            return "no scores so far!"
        
        i=0
        while i < 10 and i < len(scores_in_order_list):
            top_10_scores.append(scores_in_order_list[i])
            i += 1

        for array in top_10_scores:
            time = array[0]
            time_formatted = format_time(time)
            name = array[1]
            formatted_str += f"{time_formatted}, {name}\n"

        return formatted_str

    else:
        return make_response("Incorrect password", 404)

# Fetching all scores with limit DONE!
@app.route("/scores/limit/<int:limit>")
def get_scores_limit(limit):
    """ Returns scores within limit set in url.
    Parameters
    ----------
    Int : `limit`
        The limit that determines how many scores are shown
    Returns
    -------
        Returns 200 and scores within limit or 404 if password incorrect
    """

    password = request.args.get('pw')
    if check_api_key(password):
        all_scores_sorted = sort_score()
        scores_within_limit = []

        if limit > len(all_scores_sorted):
            return abort(404)

        i = 0
        while i < limit:
            scores_within_limit.append(all_scores_sorted[i])
            i += 1

        return make_response(scores_within_limit, 200)

    else: make_response("Incorrect password", 404)

#Delete a score DONE!
@app.route('/all_scores/<int:the_id>', methods=['DELETE'])
def delete_score(the_id):
    """ Deletes a score based on int user gives in url (if password is valid).
        Parameters
    ----------
    Int : `the_id`
        The id of the score that is being deleted.
    Returns
    -------
        204 if score was deleted, 404 if incorrect password or score not found
    """

    password = request.args.get('pw')
    if check_api_key(password):
        print(the_id)

        blob = bucket.blob('scores.json')
        score_data = blob.download_as_string()

        if score_data:
            all_data = json.loads(score_data)
        else:
            return abort(404, description= "No scores to delete!")

        try:
            del all_data['scores'][the_id-1]
            all_data = adjust_ids(all_data, the_id)

            updated_score_data = json.dumps(all_data)
            blob.upload_from_string(updated_score_data, content_type='text/plain')

            return make_response(f'Score {the_id} removed succesfully!', 204)
        except:
            return abort(404, description= "Score not found")

    else:
        make_response("Incorrect password", 404)

@app.route('/scores', methods=['POST'])
def add_highscore():
    """ Saves highscore to scores.json if password is valid. Generates id for new score
    and adds id, time and name to dict that is appended to existing scores. 
    Data is dumped to firebase.
    Returns
    -------
        Returns 'Score added successfully' 201 if score was added, 'Incorrect password' 404 if not.
    """
    password = request.args.get('pw')
    if check_api_key(password):
        blob = bucket.blob('scores.json')
        score_data = blob.download_as_string()

        if score_data:
            existing_scores = json.loads(score_data)
        else:
            existing_scores = {"scores": []}

        new_score = {}
        received_score = request.get_json()

        new_score['id'] = generate_id()
        new_score['time'] = received_score['time']
        new_score['name'] = received_score['name']
        
        existing_scores['scores'].append(new_score)

        updated_score_data = json.dumps(existing_scores)
        blob.upload_from_string(updated_score_data, content_type='text/plain')

        print(updated_score_data)

        return 'Score added successfully', 201 
    
    else:
        return make_response("Incorrect password", 404)

def sort_score(descending=False):
    """ Sorts the score into ascending or decending order with all keys included.
    Parameters
    ----------
    Boolean : `descending=False`
        Boolean value determining whether the data is shown in ascending or decending order.
        Default is False (ascending).
    Returns
    -------
       Dict of scores with ids, times and names.
    """

    all_data = read_score()
    all_scores = all_data["scores"]
    times = sorted(all_scores, key=lambda k: k["time"], reverse=descending)

    sorted_scores = []

    for score in times:
        id = score["id"]
        time = score["time"] 
        name = score["name"]
        single_score = {"id": id, "time": str(time), "name": str(name)}
        sorted_scores.append(single_score)

    return sorted_scores

def make_2D_array(descending=False):
    """ Makes a 2d list with scores ignoring time and name. 
    Method is used  with html page.
    Parameters
    ----------
    Boolean : `descending=False`
        Boolean value determining whether the data is shown in ascending or decending order.
        Default is False (ascending).
    Returns
    -------
       List of scores with times and names.
    """
    all_data = read_score()
    all_scores = all_data["scores"]

    times = sorted(all_scores, key=lambda k: k["time"], reverse=descending)
    score_list = []

    for score in times:
        time = score["time"] 
        name = score["name"]
        single_score = [str(time), str(name)]
        score_list.append(single_score)

    return score_list

def read_score():
    """ Reads scores from firebase
    Returns
    -------
        Dict with all scores.json data
    """
    blob = bucket.blob('scores.json')
    scores_data = blob.download_as_string()
    scores_data_io = io.StringIO(scores_data.decode('utf-8'))
    scores_data_json = json.load(scores_data_io)

    return scores_data_json

def generate_id():
    """ Generates id based on how many scores are currently saved.
    Returns
    -------
        New id, int.
    """
    # firebase implementation
    blob = bucket.blob('scores.json')
    score_data = blob.download_as_string()
    scores_dict = json.loads(score_data) if score_data else {"scores": []}

    new_id = len(scores_dict["scores"]) + 1

    return new_id

if __name__ == "__main__":
    app.run(debug=True)

