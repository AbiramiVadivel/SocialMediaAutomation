import tweepy,sys,time
import requests
import os
from PIL import Image

access_token = '1307741523065352193-06wAiYtkN9kMMzyzf6d7pg0kpEiND3'
access_token_secret = 'SFahWNFkAs6Ba8X1mIeR0rTlDpep6YPNZgaC8bqYYIX2B'
consumer_key = 'Dlg9QdhvtD3NrJ7qmploEgw7g'
consumer_secret = 'Ii1Vbuoqa3lyWzXydt226UuXN7DiOHjqrOAF9rLSCkJGIQhsyU'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api =tweepy.API(auth)
while True :
     api.update_with_media("animation.gif", "This is a good day" )
     time.sleep(60)
    




