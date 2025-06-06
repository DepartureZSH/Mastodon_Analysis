import json
import networkx as nx
from pathlib import Path
import re

def extract_instance_from_url(url_or_node):
    match = re.search(r'https?://([^/]+)/', url_or_node)
    return match.group(1) if match else 'unknown'

def load_replies_to_network(json_files, G:nx.DiGraph=None):
    if not G:
        G = nx.DiGraph()

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

                G.add_node(user_url)
                G.add_node(reply_to_url)

                # Add a directed edge from the replier to the user they replied to
                G.add_edge(user_url, reply_to_url, interaction="reply")

    return G


def load_boosters_favorites_to_network(json_files, G:nx.DiGraph=None):
    if not G:
        G = nx.DiGraph()

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
                data.update({"instance": extract_instance_from_url(post_author_url)})
                # Add the post author as a node
                G.add_node(post_author_url, **data)

                # Process boosters (reblogs)
                for booster in entry.get("reblogs", []):
                    if isinstance(booster, dict):  # Ensure booster is a dictionary
                        booster_url = booster.get("url")
                        # extra_values = {"instance": extract_instance_from_url(booster_url)}
                        if booster_url:
                            # G.add_node(booster_url, **booster)
                            # G.add_node(booster_url, **extra_values)
                            G.add_node(booster_url)
                            G.add_edge(booster_url, post_author_url, interaction="boost")  # Add boost edge

                # Process favourites
                for favoriter in entry.get("favourites", []):
                    if isinstance(favoriter, dict):  # Ensure favoriter is a dictionary
                        favoriter_url = favoriter.get("url")
                        if favoriter_url:
                            G.add_node(favoriter_url)
                            G.add_edge(favoriter_url, post_author_url, interaction="favorite")  # Add favorite edge
    return G


def load_interaction_network(data_dir):

    G = nx.DiGraph()

    # Get all booster/favorite and reply files
    data_path = Path(data_dir)
    booster_favorite_files = sorted(data_path.glob("boostersfavourites*.json"))
    reply_files = sorted(data_path.glob("reply*.json"))

    G = load_boosters_favorites_to_network(booster_favorite_files, G)
    G = load_replies_to_network(reply_files, G)

    return G

# load_interaction_network("/home/unnc/ZSH_Summer/Mastodon_Analysis/Analysis/Datasets/Example/livefeeds_splited/241212livefeeds_splited")