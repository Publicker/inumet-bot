import tweepy
import json
import time
import sys
import inspect

from config import *

# BOT
from bot import sendMessage, sendPhoto

# GET AUTH FOR USE TWITTER API
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET_KEY)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
api = tweepy.API(auth)

def parse_tweet(tweets):
  # Get data from the Tweet
  try:
    status = tweets[0]  
  except:
    status = tweets
  
  json_str = json.dumps(status._json)
  data = json.loads(json_str)
  return data

def get_content_tweet(data):
  try:
    content_text = data["extended_tweet"]["full_text"]
  except:
    try:
      content_text = data["full_text"]
    except:
      content_text = data["text"]
  
  # Check if the Tweet has media
  try:
    url_tweet = data["entities"]["media"][0]["url"]
    url_image = data["entities"]["media"][0]["media_url_https"]

    #Remove the link of the Tweet
    content_text = content_text.replace(url_tweet, '')
  except:
    url_tweet = f"https://twitter.com/{data['user']['screen_name']}/status/{data['id_str']}" 
    url_image = ""  

  return url_tweet, content_text, url_image

# IDs of Twitter users
# Inumet: 374503304
# me_irl_bot: 1009514640844308481
# tweets = api.user_timeline(id = 374503304, count = 1, include_rts = False, tweet_mode="extended")

# data = parse_tweet(tweets)

# print(json.dumps(data, indent=4, sort_keys=True))

# if "alerta" in content_text.lower(): 
#    print ('Alerta!')


class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
      # print ('TWEET:', status.text.encode('UTF-8'))
      # print ('FOLLOWERS:', status.user.followers_count)
      # print(status.extended_tweet['full_text'])
      
      print (f"Data getted at {time.ctime()}")
      try:
          #if is not retweetd and not a reply
          if (not status.retweeted) and ('RT @' not in status.text) and (status.in_reply_to_status_id_str is None):
            data = parse_tweet(status)
            url_tweet, content_text, url_image = get_content_tweet(data) 
            if not url_image:
              sendMessage(content_text)
            else:
              sendPhoto(url_image, f"{content_text} \n🔗 Link oficial: {url_tweet}")
            return(True)
      except BaseException as e:
        print ('Failed on data,',str(e))
        time.sleep(5)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=MyStreamListener(), tweet_mode='extended')
myStream.filter(follow=['1009514640844308481']) # ID of me_irl_bot
