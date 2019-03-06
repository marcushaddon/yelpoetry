"""Tweet and toot."""
import os
import random
import time

import requests
import tweepy

from poem_generators.red_roses import roses_are_red
from poem_generators.haiku import haiku
from poem_generators import limmerick

def toot(text: str) -> bool:
    """Make a toot."""
    host_instance = os.environ["MASTADON_INSTANCE"]
    token = os.environ['MASTADON_TOKEN']

    headers = {}
    headers['Authorization'] = 'Bearer ' + token

    data = {}
    data['status'] = text
    data['visibility'] = 'public'

    response = requests.post(
        url=host_instance + '/api/v1/statuses', data=data, headers=headers)

    if response.status_code == 200:

        return True

    else:

        return False

def tweet(text: str) -> None:
    """Tweet."""
    # personal details 
    consumer_key = os.environ['TWITTER_CONSUMER_KEY']
    consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
    access_token = os.environ['TWITTER_ACCESS_TOKEN']
    access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']
    
    # authentication of consumer key and secret 
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
    
    # authentication of access token and secret 
    auth.set_access_token(access_token, access_token_secret) 
    api = tweepy.API(auth) 
    
    # update the status 
    api.update_status(status=text) 

if __name__ == '__main__':
    print("Creating a poem...")

    choice = random.choice((
        ("a haiku:\n", generate_haiku),
        ("a limerick:\n", limmerick),
        ("", roses_are_red)
    ))

    text = choice[0] + choice[1]()
    
    mastadon_res = toot(text)
    twitter_res = tweet(text)
