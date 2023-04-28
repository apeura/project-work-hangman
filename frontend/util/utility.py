import json
import requests

#fills any gaps when a score has been deleted by fixing existing ids
def adjust_ids(dict, removed_id):
    all_data = dict
    all_scores = all_data["scores"]

    # Looping through scores and updating ids
    for score in all_scores:
        if score["id"] > removed_id:
            score["id"] -= 1

    return all_data

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

    return game_time

# Checks if new score should be added to top 50
def score_is_added_to_top50(new_score):

    new_time = new_score["time"]

    all_data = requests.get('https://hangman-highscores-amif.onrender.com/all_scores').json()

    if len(all_data["scores"]) < 50:
        return True

    sorted_scores = sorted(all_data["scores"], key=lambda x: x["time"])

    if new_time < sorted_scores[-1]["time"]:
        return True

    return False

if __name__ == "__main__":
    main()