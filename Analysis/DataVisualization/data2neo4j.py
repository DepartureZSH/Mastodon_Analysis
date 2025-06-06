from py2neo import Graph, Node, Relationship
import json
from pathlib import Path
import re

class Neo4jGraph:
    def __init__(self):
        self.neo4j_graph = Graph("bolt://localhost:7687", auth=("neo4j", "neo4j123123"))
        self.clear()
        
    def clear(self):
        self.neo4j_graph.run("MATCH (n) DETACH DELETE n")

    def clean_attr(self, attr_dict):
        """Remove or flatten properties that cannot be stored in Neo4j"""
        clean_dict = {}
        for k, v in attr_dict.items():
            if isinstance(v, (str, int, float, bool)) or v is None:
                clean_dict[k] = v
            elif isinstance(v, list):
                # Check if list of primitive
                if all(isinstance(i, (str, int, float, bool)) or i is None for i in v):
                    clean_dict[k] = v
                else:
                    # Skip complex list (e.g. list of dicts)
                    pass
            else:
                # Skip dicts or other complex types
                pass
        return clean_dict

    def add_node(self, node_for_adding, attr=None):
        if attr is None:
            attr = {}
        clean_attr_dict = self.clean_attr(attr)
        node = Node(node_for_adding, **clean_attr_dict)
        self.neo4j_graph.create(node)
        return node

    def add_edge(self, u_of_edge, v_of_edge, interaction, attr=None):
        if attr is None:
            attr = {}
        clean_attr_dict = self.clean_attr(attr)
        node = Relationship(u_of_edge, interaction, v_of_edge, **clean_attr_dict)
        self.neo4j_graph.create(node)

def extract_instance_from_url(url_or_node):
    match = re.search(r'https?://([^/]+)/', url_or_node)
    return match.group(1) if match else 'unknown'


def load_replies_to_network(json_files, G):
    if not G:
        raise("Not connected to neo4j")

    print("Loading *reply* interactions...")
    for file_path in json_files:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            for entry in data:
                # Extract the unique user IDs based on the 'url' field
                user_url = entry.get("acct", {}).get("url")
                reply_to_url = entry.get("reply_to_acct", {}).get("url")

                # Skip if required fields are missing
                if not user_url or not reply_to_url:
                    continue

                user_node = G.add_node(user_url)
                reply_node = G.add_node(reply_to_url)

                # Add a directed edge from the replier to the user they replied to
                G.add_edge(user_node, reply_node, interaction="reply")

    return G


def load_boosters_favorites_to_network(json_files, G):
    if not G:
        raise("Not connected to neo4j")

    print("Loading *booster* and *favourite* interactions...")
    for file_path in json_files:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            for entry in data:
                # Extract the account (post author) info
                post_author_url = entry.get("acct", {}).get("url")
                if not post_author_url:
                    continue
                data = entry.get("acct", {})
                instance = extract_instance_from_url(post_author_url)
                if instance == "unknown":
                    print(post_author_url)
                data.update({"instance": instance})
                # Add the post author as a node
                post_author_node = G.add_node(post_author_url, data)

                # Process boosters (reblogs)
                for booster in entry.get("reblogs", []):
                    if isinstance(booster, dict):  # Ensure booster is a dictionary
                        booster_url = booster.get("url")
                        extra_values = {"instance": extract_instance_from_url(booster_url)}
                        if booster_url:
                            # G.add_node(booster_url, **booster)
                            booster_node = G.add_node(booster_url, extra_values)
                            # G.add_node(booster_url)
                            G.add_edge(booster_node, post_author_node, interaction="boost")  # Add boost edge

                # Process favourites
                for favoriter in entry.get("favourites", []):
                    if isinstance(favoriter, dict):  # Ensure favoriter is a dictionary
                        favoriter_url = favoriter.get("url")
                        extra_values = {"instance": extract_instance_from_url(favoriter_url)}
                        if favoriter_url:
                            favoriter_node = G.add_node(favoriter_url, extra_values)
                            # G.add_node(favoriter_url)
                            G.add_edge(favoriter_node, post_author_node, interaction="favorite")  # Add favorite edge
    return G


def load_interaction_network(data_dir):

    G = Neo4jGraph()

    # Get all booster/favorite and reply files
    data_path = Path(data_dir)
    booster_favorite_files = sorted(data_path.glob("boostersfavourites*.json"))
    reply_files = sorted(data_path.glob("reply*.json"))

    G = load_boosters_favorites_to_network(booster_favorite_files, G)
    G = load_replies_to_network(reply_files, G)

    return G

if __name__ == "__main__":
    folder = Path(__file__).parent.parent.resolve()
    load_interaction_network(f"{folder}/Datasets/Example/livefeeds_splited/241212livefeeds_splited")