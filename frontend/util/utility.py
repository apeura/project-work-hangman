#match-case formatointi funtioiden sijaan?
import time, json
from datetime import datetime

#returns time name without id in asc order WIP
def format_score():
    all_data = json.loads(read_score())
    all_scores = all_data["scores"]
    all_scores_formatted = []
    id = ""
    name = ""
    time = ""
    #printtaa kaikki scoret riveittäin
    
    all_scores_string = ""

    for score in all_scores:
        print(score["id"], score["time"], score["name"])

    #print(all_scores_dict)
    DS_list = read_score()


    sorted_time_list = []
    #sorted_time_list += 


    #all_scores_formatted = sorted((time.strptime(d, "%H:%M:%S")) for d in sorted_time_list)
    
    #timees = sorted(timees, key=lambda x: time.strptime(score['time'], reverse=True))
    
    #all_scores_formatted = sorted(all_scores_formatted, key=lambda x: time.strptime(score['time'], "%H:%M:%S").time())
    return timees


def read_score():
    data = open("scores.json", "r")
    return data.read()

# Saves data to the text file as "(id),(time),(name)"
def save_to_score(id, time, name):

    scores_data = json.load(scores.json)
    new_score = {"id": id, "time": time, "name": name}
    
    with open('scores.json', 'a') as file:
        scores_data["scores"].append(new_score)
        print("done!")
        #with open("scores.json", "w") as file:
        #    json.dump(scores_data, file, indent=2)
    

# Generates
def generate_id():
    # Counts the amount of lines in the text file
    # so that the value can be used for the ID generation.
    scores_dict = json.loads(read_score())
    new_id = len(scores_dict['scores']) + 1

    return new_id
