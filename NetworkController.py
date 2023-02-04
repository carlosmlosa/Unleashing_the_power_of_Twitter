"""
This file controls the network database, new file incorporation and file reading.
All the networks are stored as gpickle
"""
import pandas as pd
import networkx as nx
import os
import pickle
import plotly.graph_objects as go
from random import random
from random import choice


class NetworkController:

    def __init__(self):
        if 'networks' not in os.listdir():
            os.mkdir('networks')

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

    def random_point(self):
        """returns a random point"""
        return [random(), random()]

    def assign_random_points(self, G):
        """
        Assigns random points to a network
        :param G: Network
        :return: the same network with node position as attributes
        """
        if 'pos' not in G.nodes._nodes[choice(list(G.nodes._nodes))].keys():
            pos = {}
            for item in G.nodes:
                pos[item] = self.random_point()
            nx.set_node_attributes(G, pos, 'pos')
        return G

    def represent(self, G, name, show=False, save=True):
        """
        Represents a network if it is not represented yet
        :param G: networkx to be represented
        :param name: name of the file to save, company by default
        :param show: boolean to show the plot, False by default
        :param save: Boolean to save the plot, True by default
        :return: nothing
        """

        G = self.assign_random_points(G)

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
