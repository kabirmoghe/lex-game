# Lex [2022 - ]
An experimental word game called [Lex](https://www.thelexgame.com/) that tests users' vocabulary in a high-stakes daily format.

This repository contains the key components of Lex, a new word game. Learn more about the game on my [blog](https://kabirmoghe.medium.com/a-new-word-game-d9552c191e2b).

## Takeaways
This project really gave me the chance to build something fun (which was a change from the theme of projects I'd focused on in the past). It allowed me to really honed in on the user experience, which is clearly super important when developing a game (especially one that could go viral) while also optimizing the back-end pieces. 

* The initial challenge meant developing a game idea that would be entertaining _and_ engaging for users. I focused on taking the basic premise of Scrabble and similar board games (where you're given a fixed set of letters and need to make words) and combined it with the speed and stakes of games like Wordle and the New York Times' Spelling Bee. This also meant going through an extensive trial and error process of getting feedback from other users about whether the game was too hard, too easy, fun, etc.
* With the [game rules](https://www.thelexgame.com) in mind, the next step was actually implementing it. I'd never really been experienced with JavaScript as a part of front-end development. Because I didn't want users to have to keep processing the requests through a Flask/python backend, I needed to adapt the approach to allow users to interact with the game using a JS/jQuery frontend that would keep track of and update game variables. With this, I got a great handle on JS/jQuery and applying it to a specific game-development purpose.
* In addition, I wanted users to be able to keep revisiting the game for the day and not lose their progress without needing an account, as the beauty of online games like Wordle lay in the quickness with which users could get started and keep playing. This meant getting involved in session storage for the first time. 

Overall, this project helped solidify many of my technical skills and forced me to pick up new ones, especially the new JS-based dynamic front-end and client-side management. More importantly, it gave me the opportunity to reverse engineer a lot of pre-existing things, find out what made them interesting, and put them together in a new (and hopefully more interesting) way. 

## Content & Architecture
* <b>Frontend</b>: HTML, JavaScript
* <b>Backend</b>: Flask (Python)
* <b>Data Storage</b>: Amazon S3
* <b>Deployment</b>: Heroku
* <b>Session Management</b>: Flask + local storage

Lex uses a python (Flask) backend and a responsive jQuery-based front-end that makes dynamic & asynchronous updates to the interface, with all graphics and UI/UX designs being entirely original. In addition to this repo's contents, scripts run daily to generate a new game for players, and the game information is stored on Amazon S3. 

### Files/Code + Significance:
* Static: images, graphics, etc.
* Templates: HTML files used in conjunction with the python backend
* Procfile: outlines procedure for running app on Heroku
* app.py: implements routes for the app and defines what happens at each page, grabs game data from S3, passes variables to the frontend
* appconfig.py: stores some credentials (not secure) for game login
* createData.py: automated script for producing new game information every day & place in S3
* readbucketdata.py: used to retrieve stored data in S3
* requirements.txt: pip libraries needed for this project

### In-depth Structure
* **Game Data**: the app generates words through **createData.py**, which creates a unique set of 8 letters (containing at least a few vowels), with each letter being assigned a point value based on its frequency in English. Then with those letters, it goes through a curates list of acceptable words (work-in-progress) and generates a list of words using today's letters. If there aren't at least 5 words in that list (the hardest, worst-case scenario), it'll recursively create another valid game. From there, it finds the metrics on each word, the best words, etc. This information is then stored as a dataframe in S3.
* **Backend**: the backend (mainly **app.py**) grabs the game data from S3 using **readbucketdata.py** and parses it into a set of variables. It also routes to certain admin pages (to log in and get access to game data easily).
* **Frontend**: the frontend receives game variables from the backend, parses the information, and populates the frontend pieces accordingly (i.e. adds the right letters to the keyboard, keeps track of the acceptable list of words, etc.). Then, it checks the local storage to see if game variables exist and grab their current state. From here, it parses all user interactions, updates the game variables, and adjusts their values in storage so that progress persists.
* **Deployment**: the app is deployed as a Flask app on Heroku
* **Design**: the entire frontend (everything from the letters to the various screens and widgets) are originally designed and have gone through many evolutions before being what they are today. A big part of this game was making the design responsive, as I realized that users would predominantly be playing the game from a phone or laptop, so I optimized the design for these two layouts specifically.

## Gameplay
Players are given 8 letters (each with a likelihood of appearing & point-value that correspond to their frequency in English) and 10 guesses to find that day's highest-scoring words. Players can afford to "waste" 5 guesses on lower-scoring words, as only their 5-best guesses ultimately contribute to their score. The game's interface looks like the following:  

<img width="1512" alt="image" src="https://github.com/kabirmoghe/wordgame/assets/64380076/b1f71502-f139-4310-9a2d-6a9c1275dc27">

Users can also toggle between "light" and "dark", play on a desktop or mobile device (on the web), and have persistent progress until the day ends (unless they willingly clear their history).

## Improvement
The game constantly goes through little iterations, especially in the following areas:
1) Improving the interface
2) Retooling the backend
3) Optimizing game storage for players
4) Adding new features (i.e. adding a login + database for users)
5) Pruning/adding words to the game's acceptible list

All users can leave feedback on the game's site [here](https://www.thelexgame.com/feedback). Several players users test the game on a day-to-day basis, and the goal is to expand its audience in the near future. Enjoy the game, and all feedback is welcome!

