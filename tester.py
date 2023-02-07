import matplotlib.pyplot as plt
import networkx as nx
from NetworkController import NetworkController
from TwitterUser import TwitterUser
from random import random
import matplotlib.pyplot as plt
import numpy as np

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


def build_graph():
   # Directed graph (edges have direction)
   G = nx.DiGraph()
   G.add_edges_from(get_followers_edges(screen_name="Luiiisoo")) #insert here the result of get_followers_edges
   G.add_edges_from(get_followers_edges(screen_name="seryi000")) #insert here the result of get_followers_edges
   G.add_edges_from(get_followers_edges(screen_name="soofibr")) #insert here the result of get_followers_edges
   G.add_edges_from(get_followers_edges(screen_name="mv_claudiaa")) #insert here the result of get_followers_edges
   G.add_edges_from(get_followers_edges(screen_name="Peedro_gh")) #insert here the result of get_followers_edges
   G.add_edges_from(get_followers_edges(screen_name="adrii_g_a_")) #insert here the result of get_followers_edges
   G.add_edges_from(get_followers_edges(screen_name="Paolacollado6")) #insert here the result of get_followers_edges
   return G

def save_bar_figure(data, file_name):
   """
      Saves histogram plot
      :param data: output networkx function
      :param file_name: name to save the image
      """
   data = sorted(data.values(),reverse=True)
   data = np.unique(data, return_counts=True)
   key =[str(round(item,3)) for item in data[0]]
   plt.bar(key,data[1])
   plt.title(file_name+" histogram")
   plt.xlabel(file_name)
   plt.ylabel("# of Nodes")
   plt.savefig("./figures/"+file_name+"_histogram")
   plt.close()


if __name__ == "__main__":
   user = TwitterUser()
   nc = NetworkController()

   # G = build_graph()
   # nc.save_network_graph(G, 'first_test')
   # nx.draw(G, pos=nx.circular_layout(G), node_color='r', edge_color='b')
   # nc.represent(G, 'first_test', show=True, save=True)
   G = nc.load_network_graph("second_test")

   # G = nx.random_lobster(100,.5,.6)


   # Metrics
   print("Edges: ",G.number_of_edges())
   print("Nodes: ",G.number_of_nodes())
   # print("Degree: ",G.degree())
   # print("Out Degree: ",G.out_degree())
   print("Order: ",G.order())
   print("Size: ",G.size())

   # Degree Distribution
   degree_sequence = sorted((d for n, d in G.degree()), reverse=True)
   fig = plt.bar(*np.unique(degree_sequence, return_counts=True))
   plt.title("Degree histogram")
   plt.xlabel("Degree")
   plt.ylabel("# of Nodes")
   # plt.show()
   plt.savefig("./figures/Degree histogram")
   plt.close()
   


   # Clustering Coefficient
   # https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.cluster.clustering.html#networkx.algorithms.cluster.clustering
   # warning all nodes have clustering = 0
   clustering = nx.clustering(G)
   save_bar_figure(clustering,"clustering")


   # Pagerank
   # Warning values with only 1 count are not visible
   pagerank=nx.pagerank(G)
   save_bar_figure(pagerank,"pagerank")


   # Diameter
   # networkx.exception.NetworkXError: Found infinite 
   # path length because the digraph is not strongly 
   # connected
   # eccentricity = nx.eccentricity(G)
   # save_bar_figure(eccentricity,"eccentricity")
   
   # Closeness
   # Warning values with only 1 count are not visible
   closeness = nx.closeness_centrality(G)
   save_bar_figure(closeness,"closeness")

   # Betweeness
   betweeness = nx.betweenness_centrality(G)
   save_bar_figure(betweeness,"betweeness")

   katz = nx.katz_centrality(G)
   save_bar_figure(katz,"katz_centrality")
   
   
   
   