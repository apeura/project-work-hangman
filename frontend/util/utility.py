#match-case formatointi funtioiden sijaan?
import json
from datetime import datetime
import os

#fix to scores.json not being found
scores_path = os.path.join(os.path.dirname(__file__), '..', '..', 'scores.json')

#returns data in asc order WIP
def sort_score(descending=False):
    all_data = json.loads(read_score())
    all_scores = all_data["scores"]
    times = sorted(all_scores, key=lambda k: k['time'], reverse=descending)
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
    times = sorted(all_scores, key=lambda k: k['time'], reverse=descending)
    score_list = []

    for score in times:
        time = score["time"] 
        name = score["name"]
        single_score = [str(time), str(name)]
        score_list.append(single_score)

    return score_list

#formats score to show only time and name + time formatting?
#
def format_score():
    all_scores = sort_score()
    scores_list = []
    # scores_string = "" 
    formatted_scores = ""

    for score in all_scores:
        #id = score["id"]
        time = score["time"]
        f_time = format_time(time) #format time --> 1 minute 15 seconds
        name = score["name"]
        score = f'{f_time} {name}' # --> 1 minute 15 seconds Jonne

        #scores_string += f'{time} {name} \n' -->      "02.11.01 Leevi \n00.33.00 Hanna \n00.22.00 Anni \n00.00.01 Leevi \n" 
        scores_list.append(score)           # -->      ["02.11.01 Leevi","00.33.00 Hanna","00.22.00 Anni","00.00.01 Leevi"]

    n = 0
    while len(scores_list) > n:
        formatted_scores += scores_list[n]  # --> "02.11.01 Leevi00.33.00 Hanna00.22.00 Anni00.00.01 Leevi"
        n += 1

    # player_score = scores_list[n].strip('\"')
    return formatted_scores

def read_score():
    data = open(scores_path, "r")
    return data.read()

# Saves data to a json file
def save_to_score(id, time, name):

    myobj = {'id': id, 'time': time, 'name': name}

    with open(scores_path) as f:
        data = json.load(f)

    data['scores'].append(myobj)

    with open(scores_path, 'w') as f:
        json.dump(data, f)

    print("saved to json!")

# Generates
def generate_id():
    # Counts the amount of lines in the text file
    # so that the value can be used for the ID generation.

    with open(scores_path, 'r') as f:
        scores_dict = json.load(f)
        new_id = len(scores_dict['scores']) + 1
    
    return new_id

def adjust_ids(dict, removed_id):
    all_data = dict
    all_scores = all_data["scores"]

    # Loop through all the scores and update the IDs
    for score in all_scores:
        if score["id"] > removed_id:
            score["id"] -= 1

    # Write the updated data back to the JSON file
    with open(scores_path, 'w') as f:
        json.dump(all_data, f)

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

    # e.g. 1 hour 3 minutes 59 seconds
    # 3 minutes 0 seconds
    # 1 minute 1 second

    return game_time

def main():
    make_2D_array()

if __name__ == "__main__":
    main()