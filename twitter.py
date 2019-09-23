import tweepy
import json
import time
import sys
import inspect
import os

from config import *

# BOT
from bot import *

if not TWITTER_API_KEY:
  TWITTER_API_KEY = os.environ.get('TWITTER_API_KEY', None)
  TWITTER_API_SECRET_KEY = os.environ.get('TWITTER_API_SECRET_KEY', None)
  TWITTER_ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN', None)
  TWITTER_ACCESS_SECRET = os.environ.get('TWITTER_ACCESS_SECRET', None)

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
  
  media = []

  # Check if the Tweet has media
  try:
    # If has more than one media
    if len(data["extended_entities"]["media"]) > 1:
      # For each media
      for element in data["extended_entities"]["media"]:
        media.append(element["media_url_https"])
    else:
      # If only have one media
      url_tweet = data["entities"]["media"][0]["url"]
      media.append(data["entities"]["media"][0]["media_url_https"])

    #Remove the link of the Tweet
    content_text = content_text.replace(url_tweet, '')
  except:
    # Tweet has no media
    url_tweet = f"https://twitter.com/{data['user']['screen_name']}/status/{data['id_str']}" 
    url_image = ""  

  return url_tweet, content_text, media

# IDs of Twitter users
# Inumet: 374503304
# me_irl_bot: 1009514640844308481
# tweets = api.user_timeline(id = 374503304, count = 1, include_rts = False, tweet_mode="extended")

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
          # If Tweet is not retweetd and not a reply
          if (not status.retweeted) and ('RT @' not in status.text) and (status.in_reply_to_status_id_str is None):
            data = parse_tweet(status)
            url_tweet, content_text, media = get_content_tweet(data) 
            # If not has any media -> Send basic message
            if not media:
              sendMessage(content_text)
            # If has more than one media -> Send a group of media
            elif len(media) > 1:
              sendMediaGroup(media, content_text)
            # If has one media -> Send only that media
            else:
              sendPhoto(media[0], f"{content_text} \n🔗 Link oficial: {url_tweet}")
            return(True)
      except BaseException as e:
        # If fail -> Log error
        print ('Failed on data,',str(e))
        time.sleep(5)

# Do server for 'Process exited with status 143' Heroku
from flask import Flask, Response

app = Flask(__name__)

@app.route('/')
@app.route('/start')
def start():
  message_to_return="Nice one 😎!"
  print(message_to_return)
  
  myStreamListener = MyStreamListener()
  myStream = tweepy.Stream(auth = api.auth, listener=MyStreamListener(), tweet_mode='extended')
  myStream.filter(follow=['1009514640844308481']) # ID of me_irl_bot

  return Response('{"message": ' + f"\"{message_to_return}\"" +'}', status=200, mimetype='application/json')

if __name__ == "__main__":
  # Starting of the development HTTP server
  # app.debug = True

  app.run(host='0.0.0.0', port=5000)
