import ijson
import json
import pandas as pd
import pathlib
folder = pathlib.Path(__file__).parent.parent.resolve()

def json_reader(file):
    data_folder = f"{folder}/Datasets/Example/livefeeds_splited/241212livefeeds_splited"
    with open(f'{data_folder}/{file}', 'r', encoding='utf-8') as f:
        for record in ijson.items(f, "item"):
            print(record.keys())
            print(record)
            break

json_reader("reply_1.json")