from flask import Flask, redirect, url_for, render_template, request, session
import game
import readbucketdata

app = Flask(__name__)
app.secret_key = 'hello'

def reset():
	if "possWords" in session:
		session.pop("possWords")
	session["maxList"] = []
	session["guesses"] = {}
	session["score"] = 0
	session["numGuesses"] =  0
	session["scoreGauge"] = ""
	session["addInfo"] = ""
	session["scorePos"] = 0
	session["oldMaxPoints"] = 0
	session["oldBestList"] = ""

@app.route("/", methods = ["GET", "POST"])
def home():

	word_info = readbucketdata.readbucketdata("letters.csv")
	old_word_info = readbucketdata.readbucketdata("oldletters.csv")

	oldMaxPoints, oldBestWords = old_word_info["maxPoints"][0], eval(old_word_info["bestWords"][0])

	letters, letterPts, maxPoints, bestWords, time = eval(word_info["letters"][0]), eval(word_info["letterPts"][0]), word_info["maxPoints"][0], eval(word_info["bestWords"][0]), word_info["time"][0]

	session["bestWordsOnly"] = [wordPair[0].title() for wordPair in bestWords]

	session["letters"] = letters
	session["maxPoints"] = int(maxPoints)

	session["oldMaxPoints"] = int(oldMaxPoints)

	if "time" not in session:
		session["time"] = time

	elif session["time"] != time:
		session["time"] = time
		reset()

	if "possWords" not in session:
		session["possWords"] = eval(word_info["possWords"][0])

	possWords = session["possWords"]

	if "score" in session:
		score = session["score"]
	else:
		session["score"] = 0
		score = session["score"]

	if "maxList" not in session:
		session["maxList"] = []

	if "oldBestList" not in session:
		session["oldBestList"] = []

	if "guesses" not in session:
		session["guesses"] = {}

	if "score" not in session:
		session["score"] = 0
 
	if "numGuesses" not in session:
		session["numGuesses"] =  0

	if "scoreGauge" not in session:
		session["scoreGauge"] = ""

	if "addInfo" not in session:
		session["addInfo"] = ""

	if "scorePos" not in session:
		session["scorePos"] = 0

	if session["numGuesses"] == 5:

		return redirect(url_for('done'))

	session["totalWords"] = "Find the top 5 words out of {} possible words\n".format(len(possWords))

	if score == maxPoints:
		scoreGauge = "{} You reached the highest possible score with ".format(game.score_gauge(score, maxPoints)[0])
		addInfo = ""

	else: 
		scoreGauge = "{} You scored {} points.".format(game.score_gauge(score, maxPoints)[0], score)
		addInfo = "Keep trying! The highest possible score was"

	session["scoreGauge"] = scoreGauge
	session["addInfo"] = scoreGauge

	session["scorePos"] = game.score_gauge(score, maxPoints)[1]

	session["maxList"] = [("{}, {}".format(bestWords[i][0].title(), bestWords[i][1])) for i in range(len(bestWords))]

	session["oldBestList"] = [("{}, {}".format(oldBestWords[i][0].title(), oldBestWords[i][1])) for i in range(len(oldBestWords))]

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

			guesses = session["guesses"]

			if (guess.title() in guesses):
				error = "Already guessed"

			session["guesses"] = {word: pts for word, pts in sorted(guesses.items(), key=lambda item: item[1], reverse = True)}
			
			return render_template("game.html", totalWords = session["totalWords"], letters = letters, guesses = session["guesses"], bestWordsOnly = session["bestWordsOnly"], error = error, score = session["score"], scorePos = session["scorePos"], oldMaxPoints = session["oldMaxPoints"], oldBestList = session["oldBestList"])

		else:

			pts = possWords[guess]
			guesses = session["guesses"]
			guesses[guess.title()] = pts
			guesses = {word: pts for word, pts in sorted(guesses.items(), key=lambda item: item[1], reverse = True)}

			session["guesses"] = guesses

			score += pts
			session["score"] = score

			scorePos = game.score_gauge(score, maxPoints)[1]

			session["scorePos"] = scorePos

			possWords.pop(guess)
			session["possWords"] = possWords

			session["totalWords"] = "Find the top 5 words out of {} possible words\n".format(len(possWords))

			if score == maxPoints:
				session["scoreGauge"] = "{} You reached the highest possible score with ".format(game.score_gauge(score, maxPoints)[0])
				session["addInfo"] = ""

			else: 
				session["scoreGauge"] = "{} You scored {} points.".format(game.score_gauge(score, maxPoints)[0], score)
				session["addInfo"] = "Keep trying! The highest possible score was"

			session["maxList"] = [("{}, {}".format(bestWords[i][0].title(), bestWords[i][1])) for i in range(len(bestWords))]
			session["oldBestList"] = [("{}, {}".format(oldBestWords[i][0].title(), oldBestWords[i][1])) for i in range(len(oldBestWords))]

			session["numGuesses"] = session["numGuesses"] + 1

			if session["numGuesses"] == 5:

				return redirect(url_for('done'))

	return render_template("game.html", totalWords = session["totalWords"], scoreGauge = session["scoreGauge"], letters = letters, guesses = session["guesses"], bestWordsOnly = session["bestWordsOnly"] , score = session["score"], scorePos = session["scorePos"], possWords = session["possWords"], time = session["time"], oldMaxPoints = session["oldMaxPoints"], oldBestList = session["oldBestList"])

@app.route("/done", methods = ["GET", "POST"])
def done():

	if request.method == "POST":

		reset()

		return redirect(url_for('home'))
	else:

		session["guesses"] = {word: pts for word, pts in sorted(session["guesses"].items(), key=lambda item: item[1], reverse = True)}

		return render_template("finished.html", totalWords = session["totalWords"], scoreGauge = session["scoreGauge"], addInfo = session["addInfo"], letters = session["letters"], guesses = session["guesses"], bestWordsOnly = session["bestWordsOnly"], score = session["score"], scorePos = session["scorePos"], maxPoints = session["maxPoints"], maxList = session["maxList"], oldMaxPoints = session["oldMaxPoints"], oldBestList = session["oldBestList"])

if __name__ == '__main__':
    app.run(debug = True)