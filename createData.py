import pandas as pd
import io
from io import StringIO
import os
import boto3
import game
from datetime import datetime

def main():

	newGame = game.create_word_info()

	word_info = pd.DataFrame([[newGame.letters, newGame.letterPts, newGame.maxPoints, newGame.bestWords, newGame.possWords]])

	word_info.columns = ["letters", "letterPts", "maxPoints", "bestWords", "possWords"]

	ts = datetime.now()

	word_info["time"] = ["{}:{}".format(ts.hour, ts.minute)]

	filename = 'letters.csv'
	bucketname = 'wordskm'
    
	csv_buffer = StringIO()
	word_info.to_csv(csv_buffer)
    
	client = boto3.client('s3')
    
	response = client.put_object(Body = csv_buffer.getvalue(), Bucket = bucketname, Key = filename)

if __name__ == '__main__':
    main()
