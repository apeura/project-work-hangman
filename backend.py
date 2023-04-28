from flask import render_template, Flask, jsonify, abort, make_response, request, json
from frontend.util.utility import *
from dotenv import load_dotenv
import os, bcrypt, tempfile, firebase_admin, io
from firebase_admin import credentials, storage

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

##############################################
# THE CODE BELOW IS COPIED FROM TOPIAS LAATU #
##############################################

# This method is used to check the validity of the password
# Sent with requests to the backend
def check_api_key(pw):

    if type(pw) != str:
        raise Exception("Give password as string object")
    
    # hashing the API_KEY that has been turned to bytes array
    # with randomly generated salt
    hash = bcrypt.hashpw(API_KEY.encode('utf-8'), bcrypt.gensalt())

    # checking password received as parameter with api key
    result = bcrypt.checkpw(pw.encode('utf-8'), hash)

    # returned values are boolean type
    return True if result else False

##############################################
# THE CODE ABOVE IS COPIED FROM TOPIAS LAATU #
##############################################

# Allow origins
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

# Fetches all scores and puts them into HTML form
@app.route('/')
def index():

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
    #return make_response("nice!", 209)

# Get all scores DONE!
# Gets all scores from firebase and shows them in json form
@app.route("/all_scores")
def get_scores():
#    password = request.args.get('pw')
#    return make_response(scores_str, 200) if check_api_key(password) else make_response("Incorrect password", 404)

    password = str(request.args.get('pw'))
    if check_api_key(password):
        blob = bucket.blob('scores.json')
        content = blob.download_as_string().decode('utf-8')
        data = json.loads(content)
        print(data)
        return jsonify(data)
    
    else:
        make_response("Incorrect password", 404)

# Get a single score based on the id DONE!
# Error 404, if the score with the value of "the_id" is not found
@app.route('/scores/<int:the_id>')
def get_score(the_id):

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

# Returns a descended or ascended order of the score list.
# Error 404 if the parameter in <order> is wrong
@app.route("/order/<string:order>", methods = ['GET'])
def get_asc_or_desc_scores(order):

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
        make_response("Incorrect password", 404)

# Fetching all scores with limit DONE!
@app.route("/scores/limit/<int:limit>")
def get_scores_limit(limit):

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


#adding a score DONE!
@app.route('/scores', methods=['POST'])
def add_highscore():
    
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
        make_response("Incorrect password", 404)

#returns data in asc order (default)
def sort_score(descending=False):

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

#Returns the scores as a list, excluding the id (id is not needed)
#So that the scores can be shown in the html page
def make_2D_array(descending=False):

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

# Loads the scores file from firebase and puts it into json format
def read_score():
    blob = bucket.blob('scores.json')
    scores_data = blob.download_as_string()
    scores_data_io = io.StringIO(scores_data.decode('utf-8'))
    scores_data_json = json.load(scores_data_io)

    return scores_data_json

def generate_id():

    ###### FIREBASE IMPLEMENTATION?
    blob = bucket.blob('scores.json')
    score_data = blob.download_as_string()
    scores_dict = json.loads(score_data) if score_data else {"scores": []}

    new_id = len(scores_dict["scores"]) + 1

    #url = "https://hangman-highscores-amif.onrender.com/all_scores"
    #response = requests.get(url)

    #if response.status_code == 200:
    #    scores_dict = response.json()
    #else:
    #    scores_dict = {"scores": []}

    new_id = len(scores_dict["scores"]) + 1

    return new_id

if __name__ == "__main__":
    app.run(debug=True)

