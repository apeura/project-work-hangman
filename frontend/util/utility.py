#match-case formatointi funtioiden sijaan?
import time, json
from datetime import datetime

#returns time name without id in asc order WIP
def format_score(descending=True):
    all_data = json.loads(read_score())
    all_scores = all_data["scores"]
    times = sorted(all_scores, key=lambda k: k['time'], reverse=descending)

    for score in times:
        print(score["id"], score["time"], score["name"])

def read_score():
    data = open("scores.json", "r")
    return data.read()

# Saves data to the text file as "(id),(time),(name)"
def save_to_score(id, time, name):
    with open('scores.json', 'r') as file:
        scores_data = json.load(file)
        new_score = {"id": id, "time": time, "name": name}
        scores_data["scores"].append(new_score)

    
        with open("scores.json", "w") as file:
            json.dump(scores_data, file, indent=2)
    
    #f.write("\n" + f"(id: {id}, time: {time}, name: {name})")
    #f.close()

# Creates a list of all current ID values
def get_id_list():
    id_all = []
    all_data = read_score()
    split_data = all_data.split('\n')
    for data in split_data:
        values = data.split(',')
        player_id = {'id': int(values[0])}
        id_all.append(player_id)

    return id_all

# Generates
def generate_id():
    # Counts the amount of lines in the text file
    # so that the value can be used for the ID generation.
    with open('scores.json') as f:
        id_line_amount = sum(1 for _ in f)
    
    new_id = id_line_amount + 1

    return new_id

    
def main():
    format_score()

if __name__ == "__main__":
    main()