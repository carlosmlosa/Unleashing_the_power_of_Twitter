import matplotlib.pyplot as plt
import networkx as nx
from NetworkController import NetworkController
from TwitterUser import TwitterUser
from random import random


def get_followers_edges(screen_name):
   """
   Returns a list of tuples with followers and the account they follow
   :param screen_name: nthe username of the account we are retrieving e.g. realmadrid  
   :param n: number of followers that will return the function
   """
   followers = user.get_account_followers(screen_name=screen_name)
   # followers = user.api.get_users_followers(1445665371176857602) #change upper line to search by id
   followers = list(followers[0])
   followers_tuples = list(map(lambda follower:(follower,screen_name),followers))
   return followers_tuples



if __name__ == "__main__":
   user = TwitterUser()
   nc = NetworkController()


   # Directed graph (edges have direction)
   G = nx.DiGraph()
   G.add_edges_from(get_followers_edges(screen_name="Luiiisoo")) #insert here the result of get_followers_edges
   G.add_edges_from(get_followers_edges(screen_name="seryi000")) #insert here the result of get_followers_edges
   G.add_edges_from(get_followers_edges(screen_name="soofibr")) #insert here the result of get_followers_edges
   G.add_edges_from(get_followers_edges(screen_name="mv_claudiaa")) #insert here the result of get_followers_edges
   G.add_edges_from(get_followers_edges(screen_name="Peedro_gh")) #insert here the result of get_followers_edges
   G.add_edges_from(get_followers_edges(screen_name="adrii_g_a_")) #insert here the result of get_followers_edges
   G.add_edges_from(get_followers_edges(screen_name="Paolacollado6")) #insert here the result of get_followers_edges

   nc.save_network_graph(G, 'first_test')
   nx.draw(G, pos=nx.circular_layout(G), node_color='r', edge_color='b')
   nc.represent(G, 'first_test', show=True, save=True)

   # Metrics
   print("Edges: ",G.number_of_edges())
   print("Nodes: ",G.number_of_nodes())
   print("Degree: ",G.degree())
   print("Out Degree: ",G.out_degree())
   print("Order: ",G.order())
   print("Size: ",G.size())
