from flask import Flask, redirect, url_for, render_template, request, session
import game
import readbucketdata
import createData
import json



app = Flask(__name__)
app.secret_key = 'hello'

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

	cutoff = bestWords[0][1]

	for i in range(5):
	    currPts = bestWords[i][1]
	    if currPts < cutoff:
	        cutoff = currPts

	topBest = [wordPair for wordPair in bestWords if wordPair[1] > cutoff]

	numAdd = 5 - len(topBest)

	topBestDict = {}

	for item in topBest:
	    topBestDict[item[0]] = item[1]

	topBest = json.dumps(topBestDict)
	bestWords = json.dumps(bestWordsDict)
	possWords = json.dumps(eval(word_info["possWords"][0]))

	oldBestWords = json.dumps(oldBestWordsDict)
	oldBestWordsOnly = list(oldBestWordsDict.keys())

	return render_template("game.html", letters = letters, letterPts = letterPts, maxPoints = maxPoints, bestWords = bestWords, lid = lid, possWords = possWords, oldMaxPoints = oldMaxPoints, oldBestWords = oldBestWords, oldBestWordsOnly = oldBestWordsOnly, topBest = topBest, numAdd = numAdd)


@app.route("/test", methods = ["GET", "POST"])
def test():

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

	cutoff = bestWords[0][1]

	for i in range(5):
	    currPts = bestWords[i][1]
	    if currPts < cutoff:
	        cutoff = currPts

	topBest = [wordPair for wordPair in bestWords if wordPair[1] > cutoff]

	numAdd = 5 - len(topBest)

	topBestDict = {}

	for item in topBest:
	    topBestDict[item[0]] = item[1]

	topBest = json.dumps(topBestDict)
	bestWords = json.dumps(bestWordsDict)
	possWords = json.dumps(eval(word_info["possWords"][0]))

	oldBestWords = json.dumps(oldBestWordsDict)
	oldBestWordsOnly = list(oldBestWordsDict.keys())

	return render_template("test.html", letters = letters, letterPts = letterPts, maxPoints = maxPoints, bestWords = bestWords, lid = lid, possWords = possWords, oldMaxPoints = oldMaxPoints, oldBestWords = oldBestWords, oldBestWordsOnly = oldBestWordsOnly, topBest = topBest, numAdd = numAdd)

## DON'T DELETE - BREAKS DOWN HTML FOR NOW

@app.route("/login", methods = ["GET", "POST"])
def login():

	lid = int(readbucketdata.readbucketdata("letters.csv")["lid"][0])

	if request.method == "POST":
		if (request.form["usr"] == "kabirmoghe") and (request.form["pwd"] == "Daod10Bgr6"):

			session["usr"] = "kabirmoghe"

			return redirect(url_for('home'))
		else:
			return render_template("invalidLogin.html", lid = lid)

	return render_template("login.html", lid = lid)

@app.route("/feedback", methods = ["GET", "POST"])
def feedback():

	lid = int(readbucketdata.readbucketdata("letters.csv")["lid"][0])

	return render_template("feedback.html", lid = lid)

@app.route("/data", methods = ["GET", "POST"])
def data():

	lid = int(readbucketdata.readbucketdata("letters.csv")["lid"][0])
	bestWords = eval(readbucketdata.readbucketdata("letters.csv")["bestWords"][0])

	if "usr" not in session:
		return redirect(url_for('home'))

	else:

		if request.method == "POST":

			createData.main()

			return redirect(url_for("home"))

		return render_template("data.html", lid = lid, bestWords = bestWords)


if __name__ == '__main__':
    app.run(debug = True)
