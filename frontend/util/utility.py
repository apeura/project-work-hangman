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
        id = score["id"]
        time = score["time"]
        name = score["name"]
        all_scores_string += f'{id} {time} {name} "\n"'

    #player_lines = all_data.split('\n')
    #for data in player_lines:
    #    values = data.split(',')
        
    #    one_player_score = {'id': int(values[0]), 'time': (values[1]), 'name': (values[2])}
    #    all_scores_dict.append(one_player_score)

     #   del values[0]#
     #   values_string = " ".join(values)
     #   values_string += '\n'
      #  all_scores += values_string

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