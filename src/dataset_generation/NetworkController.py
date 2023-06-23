"""
This file controls the network database, new file incorporation and file reading.
All the networks are stored as gpickle
"""
import pandas as pd
import networkx as nx
import os
import pickle
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from collections import defaultdict
from random import random
from random import choice
import requests

class NetworkController:

    def __init__(self):
        if 'networks' not in os.listdir():
            os.mkdir('networks')
        px.set_mapbox_access_token(open(".mapbox_token").read())
    def save_network_graph(self, G, name):
        """
        Saves network
        :param G: network to be saved
        :param name: name of the file
        :return: -
        """
        pickle.dump(G, open('networks/%s.gpickle' % name, 'wb'))

    def load_network_graph(self, name):
        """
        Loads network from json file
        :param name: name of the file to be loaded
        :return: network
        """
        with open('networks/%s.gpickle' % name, 'rb') as f:
            G = pickle.load(f)
        return G

    def save_network_representation(self, fig, name):
        """
        Saves representation given a figure and a name
        """
        if 'representations' not in os.listdir('networks'):
            os.mkdir('networks/representations')
        fig.write_html('networks/representations/%s.html' % name)

    def get_network_nodes(self, G):
        """Given a network, returns a list of the name of all its nodes"""
        nodes = []
        for node in G.nodes:
            nodes.append(node)
        return nodes

    def get_node_edges(self, G, node):
        """Given a node, returns a list of all its direct connexions"""
        edges = []
        for edge in G[node]:
            edges.append(edge)
        return edges


    def assign_network_properties(self, df, G):
        properties= ['id', 'screen_name', 'location', 'followers_count', 'friends_count', 'x', 'y', 'Party', 'State']
        # Twitter attributes
        for item in properties:
            nx.set_node_attributes(G, df.set_index('name')[item].to_dict(), item)
        return G

    def get_size(self, score, min_score, max_score, min_size=1, max_size=25):
        size = (score - min_score) / (max_score - min_score) * (max_size - min_size) + min_size
        return np.clip(size, min_size, max_size)

    def represent_senators_map(self, df, G, name, show=False, save=True):
        # Assign attributes to the network
        G = self.assign_network_properties(df, G)

        # plot nodes
        fig = px.scatter_mapbox(df,
                                lat='x',
                                lon='y',
                                color="Party",
                                hover_name='Senator',
                                hover_data=['screen_name', 'State', 'followers_count', 'friends_count'],
                                color_discrete_map={'Republican': 'red', 'Democratic': 'blue'},
                                size=df.followers_count.apply(lambda x: self.get_size(x, df.followers_count.min(), df.followers_count.max())),
                                title=name,
                                mapbox_style="carto-positron",
                                zoom=4)

        edge_x, edge_y, party_origin = [], [], []
        for edge in G.edges():
            x0, y0 = G.nodes[edge[0]]['x'], G.nodes[edge[0]]['y']
            x1, y1 = G.nodes[edge[1]]['x'], G.nodes[edge[1]]['y']
            party_origin.append(G.nodes[edge[0]]['Party'])
            party_origin.append(G.nodes[edge[0]]['Party'])
            party_origin.append(G.nodes[edge[0]]['Party'])
            edge_x.append(x0)
            edge_x.append(x1)
            edge_x.append(None)
            edge_y.append(y0)
            edge_y.append(y1)
            edge_y.append(None)
        data = pd.DataFrame({'x': edge_x, 'y': edge_y, 'Party': party_origin})


        fig.add_trace(go.Scattermapbox(name= 'Republican Follows', lat=data[data.Party == 'Republican'].x.to_list(), lon=data[data.Party == 'Republican'].y.to_list(),
                                       mode='lines', line=dict(color='#EB9988', width=0.01)))
        fig.data[-1]['showlegend'] = True
        fig.add_trace(go.Scattermapbox(name= 'Democratic Follows', lat=data[data.Party == 'Democratic'].x.to_list(), lon=data[data.Party == 'Democratic'].y.to_list(),
                                       mode='lines', line=dict(color='#A3EBFB', width=0.01)))
        fig.data[-1]['showlegend'] = True
        fig.add_trace(go.Scattermapbox(name= 'Rest of Follows', lat=data[data.Party.isin(['Democratic', 'Republican']) == False].x.to_list(),
                                       lon=data[data.Party.isin(['Democratic', 'Republican']) == False].y.to_list(),
                                       mode='lines', line=dict(color='#A7A7A7', width=0.01)))
        fig.data[-1]['showlegend'] = True

        fig.update_traces(line=dict(width=0.001))
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        fig.update_layout(annotations=[dict(
                                text="OSNA: Spring 2023, Miguel Cozar and Carlos Munoz",
                                showarrow=False,
                                xref="paper", yref="paper",
                                x=0.005, y=-0.002)],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
           title = 'US Senators Twitter Analysis',
           titlefont_size = 16
        )
        if save:
            self.save_network_representation(fig, name)
        if show:
            fig.show()
        return fig

    def count_interparty_followers(self, G):
        party_counts = defaultdict(int)
        for node in G.nodes():
            node_party = G.nodes[node]['Party']
            in_neighbors = G.in_edges(node)
            for in_neighbor in in_neighbors:
                neighbor_party = G.nodes[in_neighbor[0]]['Party']
                if neighbor_party != node_party:
                    party_counts[node] += 1
        return dict(party_counts)

    def represent_senators_by_connections(self, df, G, name):
        G = self.assign_network_properties(df, G)

        df = df.merge(pd.DataFrame(list(G.in_degree), columns=['name', 'senator_followers']), on='name')

        fig= px.scatter_mapbox(df,
                                        lat='x',
                                        lon='y',
                                        color='Party',
                                        hover_name='Senator',
                                        hover_data=['screen_name', 'State', 'followers_count', 'friends_count', 'senator_followers'],
                                        size=df.senator_followers.apply(lambda x: self.get_size(x, df.senator_followers.min(), df.senator_followers.max())),
                                        #title='Senators followers between them',
                                        color_discrete_map={'Republican': 'red', 'Democratic': 'blue'},
                                        mapbox_style="carto-positron",
                                        zoom=4)
        fig.update_layout(mapbox_style="open-street-map", margin=dict(b=20, l=5, r=5, t=40))
        self.save_network_representation(fig, name)
        return fig


    def get_interparty_representation(self, df, G, name):
        G = self.assign_network_properties(df, G)

        df = df.merge(pd.DataFrame(list(self.count_interparty_followers(G).items()), columns=['name', 'interparty_followers']), on='name')


        fig= px.scatter_mapbox(df,
                                        lat='x',
                                        lon='y',
                                        color='Party',
                                        hover_name='Senator',
                                        hover_data=['screen_name', 'State', 'followers_count', 'friends_count', 'interparty_followers'],
                                        size=df.interparty_followers.apply(lambda x: self.get_size(x, df.interparty_followers.min(), df.interparty_followers.max())),
                                        #title='Interparty connections ',
                                        color_discrete_map={'Republican': 'red', 'Democratic': 'blue'},
                                        mapbox_style="carto-positron",
                                        zoom=4)
        fig.update_layout(mapbox_style="open-street-map", margin=dict(b=20, l=5, r=5, t=40))
        self.save_network_representation(fig, name)
        return fig

    def represent(self, df, G, name, show=False, save=True):
        """
        Represents a network if it is not represented yet
        :param df: dataframe with the data of the senators
        :param G: networkx to be represented
        :param name: name of the file to save, company by default
        :param show: boolean to show the plot, False by default
        :param save: Boolean to save the plot, True by default
        :return: nothing
        """

        G = self.assign_network_properties(df, G)

        edge_x = []
        edge_y = []
        for edge in G.edges():
            x0, y0 = G.nodes[edge[0]]['pos']
            x1, y1 = G.nodes[edge[1]]['pos']
            edge_x.append(x0)
            edge_x.append(x1)
            edge_x.append(None)
            edge_y.append(y0)
            edge_y.append(y1)
            edge_y.append(None)

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')

        node_x, node_y = [], []
        for node in G.nodes():
            x, y = G.nodes[node]['pos']
            node_x.append(x)
            node_y.append(y)

        # Plot points
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            hoverinfo='text',
            hovertemplate='<i>Account info</i>:<br>%{text}',

            marker=dict(
                showscale=True,
                reversescale=False,
                color=[],
                size=10,
                colorbar=dict(
                    thickness=15,
                    title='Node Connections',
                    xanchor='left',
                    titleside='right'
                ),
                line_width=2))

        node_adjacencies = []
        node_text = []
        for node, adjacencies in enumerate(G.adjacency()):
            node = adjacencies[0]
            node_adjacencies.append(len(adjacencies[1]))
            text = 'Name: %s <br> # of followers in graph: ' % adjacencies[0] + str(len(adjacencies[1]))
            try:
                text += ' <br><br>ID: %s  <br>ScreenName: %s <br>Name: %s <br>Location: %s <br>Followers: %s <br>Friends: %s' % (
                G.nodes[node]['id'], G.nodes[node]['screen_name'],
                G.nodes[node]['name'], G.nodes[node]['location'], G.nodes[node]['followers_count'],
                G.nodes[node]['friends_count'])
                node_text.append(text)
            except:
                pass

        node_trace.marker.color = node_adjacencies
        node_trace.text = node_text

        fig = go.Figure(data=[edge_trace, node_trace],
                        layout=go.Layout(
                            title='<br>Network: %s' % name,
                            titlefont_size=16,
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=20, l=5, r=5, t=40),
                            annotations=[dict(
                                text="Python code: <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>",
                                showarrow=False,
                                xref="paper", yref="paper",
                                x=0.005, y=-0.002)],
                            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                        )

        if show:
            fig.show()
        if save:
            self.save_network_representation(fig, name)
        return fig
