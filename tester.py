import matplotlib.pyplot as plt
import networkx as nx
from NetworkController import NetworkController
from TwitterUser import TwitterUser
from random import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px

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
   relationships = pd.read_csv('relationships.csv')
   for index, row in relationships.iterrows():
    if row["relationship"] == "following":
      G.add_edge(row["person1"],row["person2"])
      G.add_edge(row["person2"],row["person1"])
    elif row["relationship"] == "following only by person1":
      G.add_edge(row["person1"],row["person2"])
    elif row["relationship"] == "following only by person2":
      G.add_edge(row["person2"],row["person1"])

   return G

def save_bar_figure(data, file_name):
   """
      Saves histogram plot
      :param data: output networkx function
      :param file_name: name to save the image
      """
   # data = sorted(data.values(),reverse=True)
   # data = np.unique(data, return_counts=True)
   # key =[str(round(item,3)) for item in data[0]]
   plt.hist(data.values())
   # print(data)
   plt.title(file_name+" histogram")
   plt.xlabel(file_name)
   plt.ylabel("# of Nodes")
   plt.savefig("./figures/"+file_name+"_histogram")
   plt.close()
#   plt.show()


def save_bar_figure_html(data, file_name):
  """
    Saves histogram plot
    :param data: output networkx function
    :param file_name: name to save the image
    """
  data = pd.DataFrame(data=data.values(),columns=[file_name])
  fig = px.histogram(data,x = file_name,title=file_name+" histogram")
  fig.write_html("./figures/"+file_name+".html")

if __name__ == "__main__":
   user = TwitterUser()
   nc = NetworkController()

   # G = build_graph()
   # nc.save_network_graph(G, 'senators')
   # nx.draw(G, pos=nx.circular_layout(G), node_color='r', edge_color='b')
   # nc.represent(G, 'senators', show=True, save=True)
   G = nc.load_network_graph("senators")


   # Metrics
   print("Edges: ",G.number_of_edges())
   print("Nodes: ",G.number_of_nodes())
   # print("Degree: ",G.degree())
   # print("Out Degree: ",G.out_degree())
   print("Order: ",G.order())
   print("Size: ",G.size())

   # Degree Distribution
   degree_sequence = sorted((d for n, d in G.degree()), reverse=True)
   plt.bar(*np.unique(degree_sequence, return_counts=True))
   plt.title("Degree histogram")
   plt.xlabel("Degree")
   plt.ylabel("# of Nodes")
   # plt.show()
   plt.savefig("./figures/Degree histogram")
   plt.close()
   ds_df = pd.DataFrame(data=degree_sequence,columns=["Degree"])
   fig = px.histogram(ds_df,x="Degree",title="Degree_histogram")
   fig.write_html("./figures/Degree histogram.html")


   # Clustering Coefficient
   # https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.cluster.clustering.html#networkx.algorithms.cluster.clustering
   clustering = nx.clustering(G)
   save_bar_figure(clustering,"clustering")
   save_bar_figure_html(clustering,"clustering")

   # Pagerank
   pagerank=nx.pagerank(G)
   save_bar_figure(pagerank,"pagerank")
   save_bar_figure_html(pagerank,"pagerank")


   # Diameter
   # networkx.exception.NetworkXError: Found infinite 
   # path length because the digraph is not strongly 
   # connected
   # eccentricity = nx.eccentricity(G)
   # save_bar_figure(eccentricity,"eccentricity")
   
   # Closeness
   closeness = nx.closeness_centrality(G)
   save_bar_figure(closeness,"closeness")
   save_bar_figure_html(closeness,"closeness")

   # Betweeness
   betweeness = nx.betweenness_centrality(G)
   save_bar_figure(betweeness,"betweeness")
   save_bar_figure_html(betweeness,"betweeness")

   

   
   
   
   