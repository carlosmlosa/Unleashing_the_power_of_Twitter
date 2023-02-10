"""
This class serves as a Twitter User and has the methods to access peoples accounts and retrieve their connections
"""
import pandas as pd
from tokens import *
import tweepy
import json
import time
import networkx as nx
from NetworkController import NetworkController
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

    def get_user(self, user_id):
        """Gets user info given its ID"""
        return self.api.get_user(user_id=user_id)._json

    def get_network_info(self, G, name, save = True):
        """
        Given a network, it tries to retrieve all the possible information about the node. It takes time so be patient
        :param G: the network
        :return: the escalated network
        """
        attributes = ['id', 'screen_name', 'name', 'location', 'followers_count', 'friends_count']
        to_retrieve = list(G.nodes._nodes.keys())
        infos = pd.DataFrame(columns = attributes)
        while to_retrieve != []:
            try:
                info = self.get_user(user_id=to_retrieve[0])
                aux = []
                for item in attributes:
                    aux.append(info[item])
                infos.loc[len(infos)] = aux
                to_retrieve.pop(0)
            except Exception as e:
                print(e)
                x = str(e)
                if '429' in x:
                    # If too many request exceeded we just wait five mintues
                    time.sleep(60*5)
                else:
                    # Otherwise we discard the information
                    to_retrieve.pop(0)
                continue
        for item in attributes:
            nx.set_node_attributes(G, dict(zip(infos.id, infos[item])), item)
        if save:
            NetworkController().save_network_graph(G, name)
        return G
