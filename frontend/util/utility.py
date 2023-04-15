#match-case formatointi funtioiden sijaan?
import time, json
from datetime import datetime

#returns data in asc order WIP
def sort_score(descending=True):
    all_data = json.loads(read_score())
    all_scores = all_data["scores"]
    times = sorted(all_scores, key=lambda k: k['time'], reverse=descending)
    sorted_scores = []

    for score in times:
        id = score["id"]
        time = score["time"] 
        name = score["name"]
        single_score = {"id": str(id), "time": str(time), "name": str(name)}
        sorted_scores.append(single_score)

    return sorted_scores

def format_score():
    all_scores = sort_score()
    scores_list = []
    # scores_string = "" 
    formatted_scores = ""

    for score in all_scores:
        #id = score["id"]
        time = score["time"] 
        name = score["name"]
        score = f'{time} {name}'

        #scores_string += f'{time} {name} \n' -->      "02.11.01 Leevi \n00.33.00 Hanna \n00.22.00 Anni \n00.00.01 Leevi \n" 
        scores_list.append(score)           # -->      ["02.11.01 Leevi","00.33.00 Hanna","00.22.00 Anni","00.00.01 Leevi"]

    n = 0

    while len(scores_list) > n:
        player_score = scores_list[n].strip('\"')
        formatted_scores += scores_list[n]# --> ["0","2",".","1","1",".","0","1"," ","L","e","e","v","i","0","0",".","3","3",".","0","0"," ","H","a","n","n","a","0","0",".","2","2",".","0","0"," ","A","n","n","i","0","0",".","0","0",".","0","1"," ","L","e","e","v","i"]
        n += 1


    # "02.11.01 Leevi 00.33.00 Hanna02.11.01 Leevi 00.33.00 Hanna02.11.01 Leevi 00.33.00 Hanna02.11.01 Leevi 00.33.00 Hanna"
    return formatted_scores

def read_score():
    data = open("scores.json", "r")
    return data.read()

# Saves data to a json file 
def save_to_score(id, time, name):

    #scores_data = json.load(scores.json)
    new_score = {"id": id, "time": time, "name": name}
    
    with open('scores.json', 'w') as file:
        json.dump(new_score, file)

        #with open("scores.json", "w") as file:
        #    json.dump(scores_data, file, indent=2)
    

# Generates
def generate_id():
    # Counts the amount of lines in the text file
    # so that the value can be used for the ID generation.
    scores_dict = json.loads(read_score())
    new_id = len(scores_dict['scores']) + 1

    return new_id
