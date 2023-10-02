# %% [markdown]
# # Solution 4

# %%
import os
import numpy as np
import pandas as pd

import os
from castle.common.priori_knowledge import PrioriKnowledge
# os.path.abspath('.')

# %%
import plotly.express as px
import plotly.graph_objects as go


# %%
from methods import *

# %% [markdown]
# # Read Data



def read_data(dataname = 'dataset_1'):
    # alarm data
    alarms = pd.read_csv(r'./datasets/dataset_1/alarm.csv')
    # causal_prior
    causal_prior= np.load(r'./datasets/dataset_1/causal_prior.npy')

    # topology
    topology = np.load(r'./datasets/dataset_1/topology.npy')

    # rca
    rca_prior = pd.read_csv(r'./datasets/dataset_1/rca_prior.csv')

    print(f"shape of alarm data: {alarms.shape}")
    print(f"shape of causal prior matrix: {causal_prior.shape}")
    print(f"shape of topology prior matrix: {topology.shape}")
    print(f"shape of rca prior matrix: {rca_prior.shape}")
    # Notes: topology.npy and rca_prior.csv are not used in this script.
    
    return alarms, causal_prior, topology, rca_prior

# %%
# dataset = 'dataset_4'



def read_data(dataset = 'dataset_1'):

    # alarm data
    alarms = pd.read_csv(r'./NeurIPS2023/datasets/{}/alarm.csv'.format(dataset))
    # causal_prior
    causal_prior= np.load(r'./NeurIPS2023/datasets/{}/causal_prior.npy'.format(dataset))

    # # topology
    topology = np.load(r'./NeurIPS2023/datasets/{}/topology.npy'.format(dataset))

    # # rca
    rca_prior = pd.read_csv(r'./NeurIPS2023/datasets/{}/rca_prior.csv'.format(dataset))

    print(f"shape of alarm data: {alarms.shape}")
    print(f"shape of causal prior matrix: {causal_prior.shape}")
    print(f"shape of topology prior matrix: {topology.shape}")
    print(f"shape of rca prior matrix: {rca_prior.shape}")
    print("_________")
    
    prior_knowledge = PrioriKnowledge(causal_prior.shape[0])
    for i, j in zip(*np.where(causal_prior == 1)):
        prior_knowledge.add_required_edge(i, j)

    for i, j in zip(*np.where(causal_prior == 0)):
        prior_knowledge.add_forbidden_edge(i, j)
    
    return alarms, causal_prior, topology, rca_prior, prior_knowledge


# Notes: topology.npy and rca_prior.csv are not used in this script.


# alarms, causal_prior, topology, rca_prior, prior_knowledge = read_data(dataset = 'dataset_1')
# alarms, causal_prior, topology, rca_prior, prior_knowledge = read_data(dataset = 'dataset_2')
# alarms, causal_prior, topology, rca_prior, prior_knowledge= read_data(dataset = 'dataset_3')
# alarms, causal_prior, topology, rca_prior = read_data(dataname = 'dataset_1')

# %%

# %% [markdown]
# 

# %% [markdown]
# # 从预处理过的数据中读取


# %%
# len(list_of_dataset), len(list_of_dataset[0])

# %% [markdown]
# # 建模


if __name__ == '__main__':
    # %%
# %%# %%
    dataset = 'dataset_1'
    
    list_of_dataset =[]
    for dataset in ['dataset_1', 'dataset_2', 'dataset_3']:
        alarms, causal_prior, topology, rca_prior, prior_knowledge = read_data(dataset = dataset)
        # print(f"dataset: {dataset}")
        # print(f"shape of alarm data: {alarms.shape}")
        # print(f"shape of causal prior matrix: {causal_prior.shape}")
        # print(f"shape of topology prior matrix: {topology.shape}")
        # print(f"shape of rca prior matrix: {rca_prior.shape}")
        # print("_________")
        
        list_of_dataset.append([dataset,alarms, causal_prior, topology, rca_prior, prior_knowledge])
        
    pre_solution = '01_topo_only_winsize_500'

    list_of_dataset =[]
    for dataset in ['dataset_1', 'dataset_2', 'dataset_3']:
        alarms, causal_prior, topology, rca_prior, prior_knowledge = read_data(dataset = dataset)
        samples = pd.read_csv(r'./NeurIPS2023/datasets_processed/{}/{}.csv'.format(pre_solution,dataset))
        # print(f"dataset: {dataset}")
        # print(f"shape of alarm data: {alarms.shape}")
        # print(f"shape of causal prior matrix: {causal_prior.shape}")
        # print(f"shape of topology prior matrix: {topology.shape}")
        # print(f"shape of rca prior matrix: {rca_prior.shape}")
        # print("_________")
        
        list_of_dataset.append([dataset,alarms, causal_prior, topology, rca_prior, prior_knowledge,samples])

    import importlib

    import methods
    importlib.reload(methods)
    from methods import Causal
    from methods import causal_all

    # %%
    causal_all(list_of_dataset = list_of_dataset, preprocessed = False)
