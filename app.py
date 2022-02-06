from flask import Flask, redirect, url_for, render_template, request
import game

app = Flask(__name__)
app.secret_key = 'hello'

# Global variables 

newGame = game.create_word_info()

guesses = {}

score = 0

numGuesses =  0

scoreGauge = ""

maxPossible = ""

maxList = []

totalWords = "Find the top 5 words out of {} possible words\n".format(len(newGame.possWords))

scorePos = 0

@app.route("/", methods = ["GET", "POST"])
def home():
	
	global guesses
	global newGame
	global numGuesses
	global score
	global maxPossible
	global maxList
	global scoreGauge
	global totalWords
	global scorePos

	#for i in range(len(newGame.letters)-1):
		#letters_are += newGame.letters[i].upper() + "({}), ".format(newGame.letterPts[i])

	#letters_are += newGame.letters[-1].upper() + "({}) ".format(newGame.letterPts[-1])


	scoreGauge = "{} You scored {} points.".format(game.score_gauge(score, newGame.maxPoints)[0], score)

	scorePos = game.score_gauge(score, newGame.maxPoints)[1]

	maxPossible = "The maximum possible score was {}, and the best possible words were:".format(newGame.maxPoints)
	maxList = [("{} ({} points)".format(newGame.bestWords[i][0].upper(), newGame.bestWords[i][1])) for i in range(len(newGame.bestWords))]

	totalWords = "Find the top 5 words out of {} possible words\n".format(len(newGame.possWords))

	if request.method == "POST":
		tile1 = request.form["1"]
		tile2 = request.form["2"]
		tile3 = request.form["3"]
		tile4 = request.form["4"]
		tile5 = request.form["5"]

		guess = (tile1 + tile2 + tile3 + tile4 + tile5).lower()

		is_word = (guess in newGame.possWords)

		if (is_word == False):

			error = "Invalid word"

			if (guess.title() in guesses):
				error = "Already guessed"
			
			return render_template("game.html", totalWords = totalWords, letters = newGame.letters, guesses = guesses, error = error, score = score, scorePos = scorePos)

		else:

			pts = newGame.possWords[guess]
			guesses[guess.title()] = pts
			score += pts

			scorePos = game.score_gauge(score, newGame.maxPoints)[1]

			newGame.possWords.pop(guess)

			totalWords = "Find the top 5 words out of {} possible words\n".format(len(newGame.possWords))

			scoreGauge = "{} You scored {} points.".format(game.score_gauge(score, newGame.maxPoints)[0], score)

			maxPossible = "The maximum possible score was {}, and the best possible words were:".format(newGame.maxPoints)
			maxList = [("{}, {}".format(newGame.bestWords[i][0].title(), newGame.bestWords[i][1])) for i in range(len(newGame.bestWords))]

			numGuesses += 1
			
			if numGuesses == 5:

				return redirect(url_for('done'))

	return render_template("game.html", totalWords = totalWords, scoreGauge = scoreGauge, letters = newGame.letters, guesses = guesses, score = score, scorePos = scorePos)

@app.route("/done", methods = ["GET", "POST"])
def done():

	global guesses
	global newGame
	global numGuesses
	global score
	global scoreGauge
	global maxPossible
	global maxList
	
	if request.method == "POST":
		guesses = {}
		numGuesses = 0
		score = 0
		newGame = game.create_word_info()
		totalWords = "Find the top 5 words out of {} possible words\n".format(len(newGame.possWords))
		maxList = []
		maxPossible = ""
		scoreGauge = ""

		return redirect(url_for('home'))
	else:
		return render_template("done.html", guesses = guesses, score = score, scoreGauge = scoreGauge, maxPossible = maxPossible, maxList = maxList)

if __name__ == '__main__':
    app.run(debug = True)