import requests
"""
Module that contains functions relating to formatting validating data
"""
def adjust_ids(dict, removed_id):
    """ Adjusts score ids after deletion has occurred so score ids have no gaps.
    Parameters
    ----------
    Dictionary : `dict`
        Dictionary that contains all scores data after deletion.
    Int : `removed_id`
        The id that was removed previously.
    Returns
    -------
        Data with corrected ids
    """
    all_data = dict
    all_scores = all_data["scores"]

    # Looping through scores and updating ids
    for score in all_scores:
        if score["id"] > removed_id:
            score["id"] -= 1

    return all_data

def format_time(game_time):
    """ Formats time from 00:00:00 to 0 minutes 0 seconds format. 
    Hours get added only if time is over 60 minutes.
    Parameters
    ----------
    String : `game_time`
        The string that gets re-formatted to 0 minutes 0 seconds format.
    Returns
    -------
        Game time in new format
    """

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

def score_is_added_to_top50(new_score):
    """ Checks if new score should be added to scores.json file. If file has less than
    50 scores of if the new score is better than the worst score on record method returns True.
    Parameters
    ----------
    Dictionary : `new_score`
        Dictionary that contains new_score data name and time.
    Returns
    -------
        Boolean value True if score should be added, False if score not.
    """

    new_time = new_score["time"]

    all_data = requests.get('https://hangman-highscores-amif.onrender.com/all_scores?pw=salasana').json()

    if len(all_data["scores"]) < 50:
        return True

    sorted_scores = sorted(all_data["scores"], key=lambda x: x["time"])

    if new_time < sorted_scores[-1]["time"]:
        return True

    return False