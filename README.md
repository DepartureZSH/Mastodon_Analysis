# Mastodon 去中心化社交网络用户行为数据采集与分析 User Behavior Data Collection and Analysis in the Decentralized Social Network Mastodon

本项目旨在基于去中心化社交网络 Mastodon，使用分布式爬虫工具采集真实用户行为数据，并开展基础的数据分析工作，探索去中心化社交网络的独特特征。

This project aims to collect real user behavior data from the decentralized social network Mastodon using distributed crawler tools and conduct basic data analysis to explore the unique characteristics of decentralized social networks.

## 项目背景 / Background

随着 Fediverse 的兴起，去中心化社交网络（如 Mastodon）成为隐私友好、反平台垄断的重要替代选择。本项目以 Mastodon 为研究平台，通过真实数据了解其用户行为模式、网络传播路径及社区特征等。

With the rise of the Fediverse, decentralized social networks like Mastodon have emerged as privacy-friendly, anti-monopoly alternatives to traditional platforms. This project uses Mastodon as the research platform to examine real-world user behavior, network diffusion patterns, and community characteristics.

## 项目步骤 / Project Steps

- Step1 部署爬虫 / Deploy Crawlers
    - 分布式爬虫 / Distributed crawler [FediLive](https://github.com/FDUDataNET/FediLive)
    - 轻量级爬虫 / Lightweight crawler [mastodoner](https://github.com/harisbinzia/mastodoner)
- Step2 数据可视化 / Data Visualization
- Step3 数据清洗 / Data Cleaning
- Step4 数据分析 / Data Analysis
- Step5 分析可视化 / Analytical Visualization

## 项目结构 / Project Structure

```bash
.
├── Analysis
│   ├── Analysis
│   │   ├── __init__.py
│   │   ├── measure.py
│   │   └── __pycache__
│   │       ├── __init__.cpython-313.pyc
│   │       └── measure.cpython-313.pyc
│   ├── DataPipline
│   │   ├── load_network.py
│   │   └── __pycache__
│   │       └── load_network.cpython-313.pyc
│   ├── Datasets
│   │   ├── Cleaned_data
│   │   │   ├── FedLive
│   │   │   └── mastodoner
│   │   ├── download.sh
│   │   ├── Example
│   │   │   ├── livefeeds
│   │   │   │   └── 241212livefeeds
│   │   │   │       ├── boostersfavourites.json
│   │   │   │       ├── livefeeds.json
│   │   │   │       └── reply.json
│   │   │   ├── livefeeds_splited
│   │   │   │   └── 241212livefeeds_splited
│   │   │   │       ├── boostersfavourites_1.json
│   │   │   │       ├── boostersfavourites_2.json
│   │   │   │       ├── boostersfavourites_3.json
│   │   │   │       ├── boostersfavourites_4.json
│   │   │   │       ├── boostersfavourites_5.json
│   │   │   │       ├── livefeeds_1.json
│   │   │   │       ├── livefeeds_2.json
│   │   │   │       ├── livefeeds_3.json
│   │   │   │       ├── livefeeds_4.json
│   │   │   │       ├── livefeeds_5.json
│   │   │   │       ├── reply_1.json
│   │   │   │       ├── reply_2.json
│   │   │   │       ├── reply_3.json
│   │   │   │       ├── reply_4.json
│   │   │   │       └── reply_5.json
│   │   │   ├── livefeeds_splited.zip
│   │   │   ├── livefeeds.zip
│   │   │   └── test
│   │   └── Raw_data
│   │       ├── FedLive
│   │       └── mastodoner
│   ├── DataVisualization
│   │   ├── data
│   │   ├── data2neo4j.py
│   │   ├── dataloader.py
│   │   ├── docker-compose.yml
│   │   ├── Dockerfile
│   │   ├── jsonloader.py
│   │   ├── logs
│   │   ├── __pycache__
│   │   │   ├── dataloader.cpython-313.pyc
│   │   │   ├── load_network.cpython-313.pyc
│   │   │   └── measure.cpython-313.pyc
│   │   ├── README.md
│   │   └── Visualization_Example.ipynb
│   ├── FediLive.ipynb
│   ├── outputs
│   │   └── FediLive
│   │       ├── cross_stats.json
│   │       ├── edge_metrics.json
│   │       ├── instance_metrics.json
│   │       └── metrics.json
│   └── run_neo4j.sh
├── FediLive # FediLive爬虫
├── mastodoner # mastodoner爬虫
├── LICENSE
├── README.md
└── requirements.txt
```

## 快速开始 / Get Started

Step1: Installation
```bash
git clone -b Multi git@github.com:FDUDataNET/FediLive.git
cd FediLive

conda create -y -n FediLive python=3.11
conda activate FediLive
pip install -r requirements.txt

# fetching user interactions from all Mastodon instances via FediLive
# ...

conda deactivate

conda create -y -n MASTODON python=3.11
conda activate MASTODON

pip install networkx py2neo
```

Step2: Reproduce FediLive via Analysis/FediLive.ipynb

    Tips: Results will be stored in folder MASTODON_Analysis/Analysis/ouputs/FediLive

Step3: Start Neo4j by running neo4j docker compose
```bash
cd Analysis
bash run_neo4j.sh
```

Step4: Visualize network by running  Analysis/DataVisualization/data2neo4j.py


## 参考资源 / References

- FediLive：Fediverse-wide Parallel Crawler
- Datasets：https://zenodo.org/records/14869106
- Reference List：https://github.com/chenyang03/Reading/wiki/OSN-Fediverse
- Mastodon API Docs：https://docs.joinmastodon.org/

## License

本项目仅用于学习与科研用途，遵循原始项目协议与开源许可。

This project is for academic and research purposes only and follows the original project licenses.