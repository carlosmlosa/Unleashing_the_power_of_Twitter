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
  fig.write_image("./figures/"+file_name+".png")

if __name__ == "__main__":
   user = TwitterUser()
   nc = NetworkController()
   G = nc.load_network_graph("senators")
   df = pd.read_csv('us_senators.csv')

   # Metrics
   print("Edges: ",G.number_of_edges())
   print("Nodes: ",G.number_of_nodes())
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
   fig.write_image("./figures/Degree_histogram.png")

   degree_dict = {n:d for n,d in G.degree()}
   degree_ordered = sorted(degree_dict.items(), key=lambda x:x[1],reverse=True)
   degree_top5 = degree_ordered[:5]

   # Clustering Coefficient
   # https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.cluster.clustering.html#networkx.algorithms.cluster.clustering
   clustering = nx.clustering(G)
   save_bar_figure(clustering,"clustering")
   save_bar_figure_html(clustering,"clustering")
   clustering_ordered = sorted(clustering.items(), key=lambda x:x[1],reverse=True)
   clustering_top5 = clustering_ordered[:5]

   # Pagerank
   pagerank=nx.pagerank(G)
   save_bar_figure(pagerank,"pagerank")
   save_bar_figure_html(pagerank,"pagerank")
   pagerank_ordered = sorted(pagerank.items(), key=lambda x:x[1],reverse=True)
   pagerank_top5 = pagerank_ordered[:5]


   # Diameter
   # networkx.exception.NetworkXError: Found infinite 
   # path length because the digraph is not strongly 
   # connected
   # diameter = nx.diameter(G)
   # save_bar_figure(diameter,"diameter")
   
   # Closeness
   closeness = nx.closeness_centrality(G)
   save_bar_figure(closeness,"closeness")
   save_bar_figure_html(closeness,"closeness")
   closenes_ordered = sorted(closeness.items(), key=lambda x:x[1],reverse=True)
   closenes_top5 = closenes_ordered[:5]

   # Betweeness
   betweeness = nx.betweenness_centrality(G)
   save_bar_figure(betweeness,"betweeness")
   save_bar_figure_html(betweeness,"betweeness")
   betweeness_ordered = sorted(betweeness.items(), key=lambda x:x[1],reverse=True)
   betweeness_top5 = betweeness_ordered[:5]

   # Top values
   print(f"Degree: {degree_top5}")
   print(f"Clustering: {clustering_top5}")
   print(f"Pagerank: {pagerank_top5}")
   print(f"Closeness: {closenes_top5}")
   print(f"Betweeness: {betweeness_top5}")

   # Representation
   nc.represent_senators_map(df, G, name= 'US_Senators_OSNA', save=True, show=False)

   

   
   
   
   