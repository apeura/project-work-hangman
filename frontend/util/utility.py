import json

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



if __name__ == "__main__":
    main()