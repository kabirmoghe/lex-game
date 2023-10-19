# Lex [2022 - ]
An experimental word game called [Lex](https://www.thelexgame.com/) that tests users' vocabulary in a high-stakes daily format.

This repository contains the key components of Lex, a new word game. Learn more about the game on my [blog](https://kabirmoghe.medium.com/a-new-word-game-d9552c191e2b).

## Content
The web app for Lex uses a python (Flask) backend and a responsive jQuery-based front-end, with all graphics and UI/UX designs being entirely original. In addition to this repo's contents, scripts run daily to generate a new game for players, and the game information is stored on Amazon S3. 

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

