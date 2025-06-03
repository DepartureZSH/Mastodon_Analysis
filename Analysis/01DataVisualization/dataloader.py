import pandas as pd
import json
import pathlib
import os
folder = pathlib.Path(__file__).parent.parent.resolve()

class MASTODON_Example:
    def __init__(self, split=False):
        if split:
            data_folder = f"{folder}/Datasets/Example/livefeeds/241212livefeeds"
        else:
            data_folder = f"{folder}/Datasets/Example/livefeeds_splited/241212livefeeds_splited"
        print(f"using dataset {data_folder}")
        self.boostersfavourites = []
        self.livefeeds = []
        self.replies = []
        for file in os.listdir(data_folder):
            if "boostersfavourites" in file:
                with open(f"{data_folder}/{file}") as f:
                    data = json.load(f)
                    self.boostersfavourites.append(data)
            # elif "livefeeds" in file:
            #     with open(f"{data_folder}/{file}") as f:
            #         data = json.load(f)
            #         self.livefeeds.append(data)
            # elif "reply" in file:
            #     with open(f"{data_folder}/{file}") as f:
            #         data = json.load(f)
            #         self.replies.append(data)

    def __len__(self):
        return len(self.boostersfavourites)

    def __getitem__(self, item):
        return self.boostersfavourites[item] 

def show_detail(value):
    if isinstance(value, list):
        if len(value) == 0:
            return f"[]"
        else:
            res = [len(value)]
            res.append(show_detail(value[0]))
            return res
    elif isinstance(value, dict):
        res = [f"{key}:{show_detail(v)}" for key, v in value.items()]
        return res
    # elif isinstance(value, torch.Tensor):
    #     return value.shape
    elif isinstance(value, (str, float, int, bool)):
        return f"(example {value})"
    else:
        return f"unkwon type: {type(value)}"

import json
import pandas as pd
from typing import Union

def json_to_dataframe(json_input: Union[str, dict], from_file: bool = False) -> pd.DataFrame:
    # 读取 JSON 数据
    if from_file:
        with open(json_input, 'r', encoding='utf-8') as file:
            data = json.load(file)
    elif isinstance(json_input, str):
        try:
            data = json.loads(json_input)
        except json.JSONDecodeError:
            raise ValueError("输入的 JSON 字符串无效。")
    elif isinstance(json_input, dict):
        data = json_input
    else:
        raise TypeError("输入必须是 JSON 字符串、字典或文件路径。")

    # 自动转换为 DataFrame
    try:
        df = pd.json_normalize(data)
    except Exception as e:
        raise ValueError(f"无法转换为 DataFrame: {e}")

    return df

def json_to_dataframe(json_input: Union[str, dict], from_file: bool = False) -> pd.DataFrame:
    # 读取 JSON 数据
    if from_file:
        with open(json_input, 'r', encoding='utf-8') as file:
            data = json.load(file)

# data = MASTODON("Example/livefeeds/241212livefeeds")
# print(show_detail(data[0]))
# print(show_detail(data[0][0]))

# df = json_to_dataframe(f"{folder}/Datasets/Example/livefeeds_splited/241212livefeeds_splited/boostersfavourites_1.json", from_file=True)
# print(df.columns)