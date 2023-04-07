#match-case formatointi funtioiden sijaan?
import time

def format_score():
    all_data = read_score()
    all_scores = ""
    all_scores_dict = []

    player_lines = all_data.split('\n')
    for data in player_lines:
        values = data.split(',')
        
        one_player_score = {'id': int(values[0]), 'time': (values[1]), 'name': (values[2])}
        all_scores_dict.append(one_player_score)

        del values[0]
        values_string = " ".join(values)
        values_string += '\n'
        all_scores += values_string

    print(all_scores_dict)

    sorted((time.strptime(d, "%H:%M:%S")))
    #regex intm / ints 2 loops? to find smallest time

    return all_scores


def read_score():
    data = open("scores.txt", "r")
    return data.read()



# Saves data to the text file as "(id),(time),(name)"
def save_to_score(id, time, name):
    f = open("scores.txt", "a")
    f.write(f"\n{id},{time},{name}")
    f.close()

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
    with open('scores.txt') as f:
        id_line_amount = sum(1 for _ in f)
    
    new_id = id_line_amount + 1

    return new_id

    