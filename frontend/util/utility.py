#match-case formatointi funtioiden sijaan?
import json
from datetime import datetime
import os

#fix to scores.json not being found, determined path
scores_path = os.path.join(os.path.dirname(__file__), '..', '..', 'scores.json')
#scores_path = os.path.join(os.path.dirname(__file__), '..', 'scores.json')

#returns data in asc order (default)
def sort_score(descending=False):
    all_data = json.loads(read_score())
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

#returns list without the id
def make_2D_array(descending=False):
    all_data = json.loads(read_score())
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
    data = open(scores_path, "r")
    return data.read()


 # Saves data to a json file
def save_to_score(user_data):
    if not os.path.exists(scores_path):
        with open(scores_path, "w") as f:
            json.dumps({"scores": []}, f)

    with open(scores_path) as f:
        data = json.load(f)

    data["scores"].append(user_data)
    print("USER_DATA IN SAVE_TO_SCORE: ", user_data)
    print("DATA SAVE_TO_SCORE: ", data)
    
    with open(scores_path, 'w') as f:
        json.dumps(data, f, indent=4, ensure_ascii=False)

    print("saved to json!")

# Checks if new score should be added to top 50
def score_is_added_to_top50(new_score):

    new_time = new_score["time"]
    print("SCORE_IS_ADDED new_time is", new_time)

    with open(scores_path) as f:
        user_data = json.load(f)
        print("SCORE_IS_ADDED... USER_DATA", user_data)
    f.close()

    if len(user_data["scores"]) < 50:
        # There are less than 50 scores, so this score should be added
        return True

    # Sort the scores by time
    sorted_scores = sorted(user_data["scores"], key=lambda x: x["time"])

    # If the new score is better than the worst score in the top 50, add it
    if new_time < sorted_scores[-1]["time"]:
        return True

    # Otherwise, don't add the score
    return False

# Generates id
def generate_id():
    # Counts the amount of lines in the text file
    # so that the value can be used for the ID generation.

    with open(scores_path, 'r') as f:
        scores_dict = json.load(f)
        new_id = len(scores_dict["scores"]) + 1
    
    return new_id

#fills any gaps when a score has been deleted by fixing existing ids
def adjust_ids(dict, removed_id):
    all_data = dict
    all_scores = all_data["scores"]

    # Looping through scores and updating ids
    for score in all_scores:
        if score["id"] > removed_id:
            score["id"] -= 1

    with open(scores_path, 'w') as f:
        json.dump(all_data, f, ensure_ascii=False)

# format game time from 00:00:00 to e.g. 1minute 20seconds
# hours added only if time is over an hour
def format_time(game_time):

    # Split the time string into hours, minutes, and seconds
    hours, minutes, seconds = map(int, game_time.split(':'))

    time_components = []

    if hours > 0:
        time_components.append(f"{hours} hour{'s' if hours > 1 else ''}")
    
    if minutes == 1:
        time_components.append(f"{minutes} minute")
    else:
        time_components.append(f"{minutes} minutes")

    if seconds == 1:
        time_components.append(f"{seconds} second")
    else:
        time_components.append(f"{seconds} seconds")

    game_time = " ".join(time_components)

    # 1 hour 3 minutes 59 seconds
    # 3 minutes 0 seconds
    # 1 minute 1 second

    return game_time
