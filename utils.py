import sys
import time
from datetime import datetime
from termcolor import colored
import re
import json
from bson.json_util import dumps,loads

def delete_last_lines(n):
    "Use this function to delete the last line in the STDOUT"

    for i in range(n):
    	#cursor up one line	
	    sys.stdout.write('\x1b[1A')

	    #delete last line
	    sys.stdout.write('\x1b[2K')


def check_input_string(lst):
	for i in lst:
		if not len(i)>0:
			return False
	return True


################################ Post Tweet Functions #########################
def extract_hashtags(tweet):
	regex = "#\w+"
	lst = re.findall(regex,tweet)
	if lst:
		return lst 
	return []

def post_tweet(db,tweet,username):
	hashtags = extract_hashtags(tweet)
	tweet = {
		'tweet':tweet,
		'username':username,
		'hashtags':hashtags,
		'timestamp':datetime.now(),
		'retweeted':None,
		'retweeted_from':None,
		}
	db.tweets.insert_one(tweet)
	return True


###############################################################################

################################## Profile Functions #########################

def get_tweets(db,username):
	tweets = list(db.tweets.find({'username':username}))
	tweets.sort(key = lambda x:x['timestamp'],reverse =True)
	lst = [{"tweet":i['tweet'],'_id':i['_id'],'timestamp':i['timestamp']} for i in tweets]
	return lst

def del_tweet_by_id(db,tweet_id):
	try:
		db.tweets.delete_one({'_id':tweet_id})
		return True
	except:
		return False

	



# from pymongo import MongoClient
# client = MongoClient('localhost',27017)
# db = client.minitweet
# tweets = get_tweets(db,'rohit')
# tweets = dumps(tweets)
# # print(tweets)
# tweets = loads(tweets)
# print(tweets[0]['timestamp'])