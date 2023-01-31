"""
This class serves as a Linkedin User and has the methods to access peoples accounts and retrieve their connections
"""
from tokens import *
import tweepy
import json

class TwitterUser:

    def __init__(self):
        """An API instance is created so it is used for the rest of the methods to perform each action"""
        auth = tweepy.OAuth1UserHandler(consumer_key_public, consumer_key_private, access_token_public,
                                        access_token_private)
        self.api = tweepy.API(auth)

    def search_user(self, query) -> json:
        """Only one user"""
        return self.api.search_users(query)[0]._json

    def get_account_followers(self, screen_name, page=-1) -> list:
        """
        Gets a list of users of some account. Since there are accounts with many followers, we have to specify the pagination
        :param page: number of page to get (like if we were on the web)
        :param screen_name: the username of the account we are retrieving e.g. realmadrid IMPORTANT: to get the info of each you have to specify ._json after each user
        """
        return self.api.get_follower_ids(screen_name=screen_name, cursor=page)

    def get_account_friends(self, screen_name, page=-1) -> list:
        """
        Gets a list of friends of some account. Since there are accounts with many followers, we have to specify the pagination
        friends means mutual follows
        :param page: number of page to get (like if we were on the web)
        :param screen_name: the username of the account we are retrieving e.g. realmadrid
        :return a list of users. IMPORTANT: to get the info of each you have to specify ._json after each user
        """
        return self.api.get_friends(screen_name=screen_name, cursor=page)

    def search_users(self, query, maximum=20) -> list:
        """
        Gets list of users given a query
        :param query: query to perform
        :param maximum: max number of accounts
        :return: a list of users. IMPORTANT: to get the info of each you have to specify ._json after each user
        """
        return self.api.search_users(query, count=maximum)

