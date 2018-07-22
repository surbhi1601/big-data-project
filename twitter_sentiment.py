import  tweepy
from textblob  import TextBlob
import matplotlib.pyplot as plt

import key
# import mpld3

#  to connect with API 
consumer_key = key.twitter_consumer_key
consumer_sec = key.twitter_consumer_sec
#  to get token 
access_token = key.twitter_access_token
access_secret = key.twitter_access_secret
#  sending  consumer key and secret for check 
check=tweepy.OAuthHandler(consumer_key,consumer_sec)
#  NOW setting get_tokens
#print(dir(check))
check.set_access_token(access_token,access_secret)
#  by using  check we can connect to search api 
connected=tweepy.API(check)
#  now searching 

def checksentiment(userid, usertext, no_tweets):
	output=connected.search(usertext,count=no_tweets)
	# extracting  text words  
	positive=0
	negative=0
	neutral=0
	polarity=0

	for i in  output:
		sample=i.text
		blob_data=TextBlob(sample)
		x=blob_data.sentiment
	    #print(x)
	   # polarity+=analysis.sentiment.polarity
		if(x.polarity == 0):
	        	neutral+=1
		elif(x.polarity < 0):
			negative+=1
		elif(x.polarity > 0):
			positive+=1

		else:
			print("ERROR IN THE TEXT BLOB")


	pos=positive
	neg=negative
	neu=neutral

	# FOR THE BAR GRAPH OF REVIEWS

	left=[0.5,1.0,1.5]
	height=[pos,neg,neu]
	tick_label=['POSITIVE','NEGATIVE','NEUTRAL']
	plt.bar(left,height,tick_label=tick_label,width=0.2,color=['yellowgreen','red','green'])
	plt.ylabel('No. of tweets analyzed - '+ str(no_tweets))
	plt.xlabel('You searched for ' + usertext)
	plt.savefig("./static/img/"+userid+".png")
	plt.close()
