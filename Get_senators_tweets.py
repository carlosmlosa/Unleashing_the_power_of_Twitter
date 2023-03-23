import pandas as pd
from tokens import *
import tweepy
import json
from TwitterUser import TwitterUser

# Import senators df
us_senators_df = pd.read_csv("us_senators.csv")

# Authentication for tweepy 
auth = tweepy.OAuth1UserHandler(consumer_key_public, consumer_key_private, access_token_public,
                                access_token_private)
api = tweepy.API(auth)



def get_senator_tweets(senator_screen_name):
    tweets = api.user_timeline(screen_name=senator_screen_name, 
                            # 200 is the maximum allowed count
                            count=200,
                            include_rts = False,
                            # Necessary to keep full_text 
                            # otherwise only the first 140 words are extracted
                            tweet_mode = 'extended'
                            )
    tweets = [tweet._json for tweet in tweets]
    return tweets


def add_tweets_to_df(tweets,df):
    """This function takes a list of tweets and adds it to the dataframe df"""
    for tweet in tweets:
        row = [tweet[key] for key in headers]
        df.loc[len(df.index)] = row
    return df


headers = [
    "created_at",
    "full_text",
    "created_at",
    "coordinates",
    "place",
    "retweet_count",
    "retweeted",
    "favorite_count",
    "favorited",
    "lang"
]
tweets_df = pd.DataFrame(columns=headers)


for i in range(len(us_senators_df)):
    avoid = ["GovRicketts"]
    if us_senators_df.iloc[i].screen_name not in avoid:
        tweets = get_senator_tweets(us_senators_df.iloc[i].screen_name)
        tweets_df = add_tweets_to_df(tweets,tweets_df)
        print(tweets_df.iloc[-5:])
        print(us_senators_df.iloc[i].screen_name)
        print(i)

tweets_df.to_csv("tweets.csv")
print(tweets_df.describe())
