import ijson
import json
import pandas as pd
import pathlib
folder = pathlib.Path(__file__).parent.parent.resolve()

def json_reader(file):
    data_folder = f"{folder}/Datasets/Example/livefeeds_splited/241212livefeeds_splited"
    with open(f'{data_folder}/{file}', 'r', encoding='utf-8') as f:
        i = 0
        for record in ijson.items(f, "item"):
            i += 1
            for reblog in record["reblogs"]:
                if not isinstance(reblog, dict):
                    pass
                elif reblog.get("roles", 0):
                    print(reblog.get("roles", 0))
                    return
            for favourite in record["favourites"]:
                if favourite.get("roles", 0):
                    print(favourite.get("roles", 0))
            acct = record["acct"]
            if acct.get("roles", 0):
                print(acct.get("roles", 0))
        if i == 10000:
            return


json_reader("boostersfavourites_2.json")