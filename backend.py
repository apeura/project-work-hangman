from flask import render_template, Flask, jsonify, abort, make_response, request, json
import os
import bcrypt
from frontend.util.utility import *
from dotenv import load_dotenv

bucket = initialize_app()

app = Flask(__name__)
load_dotenv()

API_KEY = os.environ.get('API_KEY')
json_str = os.environ.get('firebase')

with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
    f.write(json_str)
    temp_path = f.name

# luetaan tiedostosta json filu
cred = credentials.Certificate(temp_path)

# tee render.comiin ympäristömuuttuja bucket, jonka sisältö
# esim: mydatabase-38cf0.appspot.com
firebase_admin.initialize_app(cred, {
    'storageBucket': os.environ.get('bucket')
})

bucket = storage.bucket()
scores_str = read_score()

# this method is used to check the validity of the password
# sent with requests to the backend
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

#Allow origins
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

#Fetch all scores
@app.route('/')
def index():
    #2D array
    scores_list = make_2D_array()
    scores_string = ""

    if len(scores_list) == 0:
        return render_template('index.html', scores="-", time="-", name="-")

    i = 0
    while i < len(scores_list):
    #for score in scores_list:
        time = str(scores_list[i][0])
        name = str(scores_list[i][1])
        scores_string += (f'{time}, {name}\n')
        i = i + 1
    
    rows = scores_string.split('\n')

    table_data = [row.split(',') for row in rows]

    return render_template('index.html', scores=table_data, time=time, name=name)
    #return make_response("nice!", 209)

#Get all scores DONE!
@app.route("/all_scores")
def get_scores():

#    password = request.args.get('pw')
#    return make_response(scores_str, 200) if check_api_key(password) else make_response("Incorrect password", 404)

    blob = bucket.blob('scores.json')
    content = blob.download_as_string().decode('utf-8')
    data = json.loads(content)
    print(data)
    return jsonify(data)


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
@app.route("/order/<string:order>", methods = ['GET'])
def get_asc_or_desc_scores(order):
    if order == "asc":
        return make_response(sort_score(False))
    
    if order == "desc":
        return make_response(sort_score(True))

    else:
        return abort(404, description="Order must be 'asc' or 'desc'")

@app.route("/scores/formatted")
def return_scores_in_format():
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

    blob = bucket.blob('scores.json')
    score_data = blob.download_as_string()
    if score_data:
        existing_scores = json.loads(score_data)
    else:
        existing_scores = {"scores": []}

    new_score = request.get_json()
    existing_scores['scores'].append(new_score)

    #scores_object = {"scores": existing_scores}

    updated_score_data = json.dumps(existing_scores)
    blob.upload_from_string(updated_score_data, content_type='text/plain')


    #print("NEW SCORE  ", new_score, "existing scores  ", existing_scores)
    #existing_scores['scores'].append(new_score)  
    #print("existing scores  ", existing_scores)

    #updated_score_data = json.dumps(existing_scores)
    #blob.upload_from_string(updated_score_data, content_type='text/plain')

    print(updated_score_data)

    return 'Score added successfully', 201 



if __name__ == "__main__":
    app.run(debug=True)