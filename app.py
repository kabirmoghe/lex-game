from flask import Flask, redirect, url_for, render_template, request, session
import game
import readbucketdata

app = Flask(__name__)
app.secret_key = 'hello'


@app.route("/", methods = ["GET", "POST"])
def home():

	word_info = readbucketdata.readbucketdata()

	letters, letterPts, maxPoints, bestWords = eval(word_info["letters"][0]), eval(word_info["letterPts"][0]), word_info["maxPoints"][0], eval(word_info["bestWords"][0])

	if "possWords" not in session:
		session["possWords"] = eval(word_info["possWords"][0])

	possWords = session["possWords"]

	if "score" in session:
		score = session["score"]
	else:
		session["score"] = 0
		score = session["score"]

	if "maxPossible" not in session:
		session["maxPossible"] = ""

	if "maxList" not in session:
		session["maxList"] = []

	if "guesses" not in session:
		session["guesses"] = {}

	if "score" not in session:
		session["score"] = 0
 
	if "numGuesses" not in session:
		session["numGuesses"] =  0

	if "scoreGauge" not in session:
		session["scoreGauge"] = ""

	if "scorePos" not in session:
		session["scorePos"] = 0

	if "totalWords" not in session:
		session["totalWords"] = "Find the top 5 words out of {} possible words\n".format(len(possWords))

	scoreGauge = "{} You scored {} points.".format(game.score_gauge(score, maxPoints)[0], score)

	session["scoreGauge"] = scoreGauge

	session["scorePos"] = game.score_gauge(score, maxPoints)[1]

	session["maxPossible"] = "The maximum possible score was {}, and the best possible words were:".format(maxPoints)
	session["maxList"] = [("{} ({} points)".format(bestWords[i][0].upper(), bestWords[i][1])) for i in range(len(bestWords))]

	session["totalWords"] = "Find the top 5 words out of {} possible words\n".format(len(possWords))

	if request.method == "POST":
		tile1 = request.form["1"]
		tile2 = request.form["2"]
		tile3 = request.form["3"]
		tile4 = request.form["4"]
		tile5 = request.form["5"]

		guess = (tile1 + tile2 + tile3 + tile4 + tile5).lower()

		is_word = (guess in possWords)

		if (is_word == False):

			error = "Invalid word"

			if (guess.title() in session["guesses"]):
				error = "Already guessed"
			
			return render_template("game.html", totalWords = session["totalWords"], letters = letters, guesses = session["guesses"], error = error, score = session["score"], scorePos = session["scorePos"])

		else:

			pts = possWords[guess]
			guesses = session["guesses"]
			guesses[guess.title()] = pts

			session["guesses"] = guesses

			score += pts
			session["score"] = score

			scorePos = game.score_gauge(score, maxPoints)[1]

			session["scorePos"] = scorePos

			possWords.pop(guess)
			session["possWords"] = possWords

			session["totalWords"] = "Find the top 5 words out of {} possible words\n".format(len(possWords))

			session["scoreGauge"] = "{} You scored {} points.".format(game.score_gauge(score, maxPoints)[0], score)

			session["maxPossible"] = "The maximum possible score was {}, and the best possible words were:".format(maxPoints)
			session["maxList"] = [("{}, {}".format(bestWords[i][0].title(), bestWords[i][1])) for i in range(len(bestWords))]

			session["numGuesses"] = session["numGuesses"] + 1
			
			if session["numGuesses"] == 5:

				return redirect(url_for('done'))

	return render_template("game.html", totalWords = session["totalWords"], scoreGauge = session["scoreGauge"], letters = letters, guesses = session["guesses"], score = session["score"], scorePos = session["scorePos"])

@app.route("/done", methods = ["GET", "POST"])
def done():

	if request.method == "POST":

		session.pop("possWords")
		session["maxPossible"] = ""
		session["maxList"] = []
		session["guesses"] = {}
		session["score"] = 0
		session["numGuesses"] =  0
		session["scoreGauge"] = ""
		session["scorePos"] = 0

		return redirect(url_for('home'))
	else:
		return render_template("done.html", guesses = session["guesses"], score = session["score"], scoreGauge = session["scoreGauge"], maxPossible = session["maxPossible"], maxList = session["maxList"])

if __name__ == '__main__':
    app.run(debug = True)