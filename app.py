from flask import Flask, redirect, url_for, render_template, request, session
import game
import readbucketdata
import createData
import json



app = Flask(__name__)
app.secret_key = 'hello'

def reset():
	if "possWords" in session:
		session.pop("possWords")
	session["maxList"] = []
	session["guesses"] = {}
	session["bestGuesses"] = {}
	session["score"] = 0
	session["numGuesses"] =  0
	session["scoreGauge"] = ""
	session["scorePos"] = 0
	session["oldScorePos"] = 0
	session["oldMaxPoints"] = 0
	session["oldBestList"] = ""
	session["status"] = "not done"
	session["level"] = ""
	session["slide"] = ""
	session["totalWords"] = ""

@app.route("/", methods = ["GET", "POST"])
def home():

	session.permanent = True

	word_info = readbucketdata.readbucketdata("letters.csv")
	old_word_info = readbucketdata.readbucketdata("oldletters.csv")

	oldMaxPoints, oldBestWords = old_word_info["maxPoints"][0], eval(old_word_info["bestWords"][0])

	letters, letterPts, maxPoints, bestWords, lid = eval(word_info["letters"][0]), eval(word_info["letterPts"][0]), int(word_info["maxPoints"][0]), eval(word_info["bestWords"][0]), int(word_info["lid"][0])

	# Turns bestWords into dictionary so it can be turned into JSON 

	bestWordsDict = {}

	for item in bestWords:
	    bestWordsDict[item[0]] = item[1]

	oldBestWordsDict = {}

	for item in oldBestWords:
	    oldBestWordsDict[item[0]] = item[1]

	bestWords = json.dumps(bestWordsDict)
	possWords = json.dumps(eval(word_info["possWords"][0]))

	oldBestWords = json.dumps(oldBestWordsDict)
	oldBestWordsOnly = list(oldBestWordsDict.keys())

	return render_template("game.html", letters = letters, letterPts = letterPts, maxPoints = maxPoints, bestWords = bestWords, lid = lid, possWords = possWords, oldMaxPoints = oldMaxPoints, oldBestWords = oldBestWords, oldBestWordsOnly = oldBestWordsOnly)


## DON'T DELETE - BREAKS DOWN HTML FOR NOW

@app.route("/login", methods = ["GET", "POST"])
def login():

	if request.method == "POST":
		if (request.form["usr"] == "kabirmoghe") and (request.form["pwd"] == "Daod10Bgr6"):

			session["usr"] = "kabirmoghe"

			return redirect(url_for('home'))
		else:
			return render_template("invalidLogin.html", lid = session["lid"])

	return render_template("login.html", lid = session["lid"])

@app.route("/feedback", methods = ["GET", "POST"])
def feedback():

	lid = readbucketdata.readbucketdata("letters.csv")["lid"][0]

	return render_template("feedback.html", lid = lid)

@app.route("/data", methods = ["GET", "POST"])
def data():

	lid = readbucketdata.readbucketdata("letters.csv")["lid"][0]

	if "usr" not in session:
		return redirect(url_for('home'))

	else:

		if request.method == "POST":

			createData.main()

			return redirect(url_for("home"))

		return render_template("data.html", lid = lid)


if __name__ == '__main__':
    app.run(debug = True)