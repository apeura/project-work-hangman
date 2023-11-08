# Hangman project with RESTful API implementation
This repository is made for a hangman game with highscore that is stored in the cloud. The game goes through three rounds of hangman (given the player is able to guess the secret words) at the end of which the player's score is saved and displayed if it's good enough. The score is saved to a database using Firebase and the server is hosted on Render, top 50 best scores are kept and displayed.

User may send http requests to add, delete and get scores in different forms if they know the relevant password.

### Examples of request urls that are available
```
get all stored data:
  GET https://hangman-highscores-amif.onrender.com/all_scores
 
delete score based on id:
  DELETE https://hangman-highscores-amif.onrender.com/all_scores/1
  
post a new score:
  POST https://hangman-highscores-amif.onrender.com/scores
 
show scores within limit:
  GET https://hangman-highscores-amif.onrender.com/scores/limit/2
  
show scores in descending order:
  GET https://hangman-highscores-amif.onrender.com/order/desc
```

This project is a part of TAMK's Python programming module and was made by Anni Peura and Leevi Heikkinen.
# Author
Anni Peura :shipit:

# Screenshots
![Hangman game win](https://user-images.githubusercontent.com/113358099/235179778-35753261-36dd-428a-93d2-1211604dd15b.jpg)

# Tech/framework used 
```
Language: Python, HTML
Web Framework: Flask
Backend Database: Firebase
Cloud platform: Render
```

# Installation and running
```
# clone repository
git clone https://github.com/apeura/project-work-hangman
cd project-work-hangman

# start frontend with python or python3 depending on your python version
python3 frontend/hangman.py
```

API implementation
API is deployed to cloud and can be accessed using following url:
https://hangman-highscores-amif.onrender.com/

### Author's note
A few potential bugs were noticed:
  - When player loses the game the last picture doesn't print
  - score_is_added_to_top50 function should delete the worst score so there are no conflicts with adding the new score

These oversights are minor and can be patched relatively easily.
