### Source: https://github.com/m-newhauser/distilbert-senator-tweets/blob/main/notebooks/get_tweets.ipynb
from datetime import datetime
import pandas as pd
import snscrape
from snscrape.modules import twitter


data = pd.read_csv('us_senators.csv')
usernames = data['screen_name']


def extract_tweets(scraped_profile, max_tweets=10000):
    """Extracts essential tweet data from a Twitter
    profile that's been previously scraped with snscrape.

    Args:
        scraped_profile (generator): Complete Twitter user profile.
    Returns:
        list: List of dictionaries each containing tweet data.
    """
    i = 0
    tweet_list = []
    for tweet in scraped_profile:
       if not isinstance(tweet, twitter.Tombstone):
          tweet_list.append(
              {
                  "date": tweet.date.strftime("%Y-%m-%d %I:%M:%S %p"),
                  "id": tweet.id,
                  "username": tweet.user.username,
                  "text": tweet.content,
                  "is_retweet": str(tweet.retweetedTweet),
                  "retweets": tweet.retweetCount,
                  "likes": tweet.likeCount
              }
           )
       i+=1
       if i >= max_tweets:
           break
    return tweet_list



def tidy_tweets(tweets):
    """Clean up raw tweet data and store in a dataframe
    with senator usernames and party affiliations.

    Args:
        tweets (list): List of dictionaries each containing tweet data.

    Returns:
        pd.DataFrame: Dataframe with all tweets for each senator as
        well as their username and party affiliation.
    """
    # Put tweet data into a df
    tweets_df = pd.DataFrame(tweets)
    # Tidy up
    return (
        tweets_df.query('is_retweet == "None"')  # remove all retweets
        .assign(date=pd.to_datetime(tweets_df.date))  # convert col from str to datetime
        # .query(f"{START_DATE} < date < {END_DATE}")  # drop tweets outside of date range
        .drop(columns=["is_retweet"])  # drop col
        .sort_values(by=["date"])  # sort by date
        .reset_index(drop=True)
    )


# Initalize empty list for tweets data
dfs = []

# Initialize empty list for skipped usernames
skipped_usernames = []

# Get tweets by username and append to db
for username in usernames.to_list():
    try:
        print(f'Extracting tweets for senator {username}')
        # Get all tweets for given username
        scraped_profile = twitter.TwitterProfileScraper(user=username).get_items()
        # Extra tweet metadata
        tweets = extract_tweets(scraped_profile)
        # Tidy up tweets and put in df
        tweets_df = tidy_tweets(tweets)
        # Append to list
        dfs.append(tweets_df)
        print(tweets_df)
        df = pd.concat(dfs)
        df.to_csv('tweet_dataset.csv', index=False)
    except Exception as e:
        print(e)
        print(f"Couldn't get tweets for {username}")
        # Get list of all skipped usernames
        skipped_usernames.append(username)



df = pd.concat(dfs)
df.to_csv('tweet_dataset.csv', index=False)
