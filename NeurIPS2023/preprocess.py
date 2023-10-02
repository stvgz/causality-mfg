
# -----------------  Pipeline ----------------- #

import pandas as pd

import plotly.express as px

class PreProcess():
    
    def __init__(self):
        self.data = None
        
    
    def remove_alarm_over_n(self,n=10000):
        """Remove"""
        
        
    def topo_close(self, level = 1):
        """"""




def start_with_x(topology, x = 0, level_to_search = 2):
    """从deviceid 为x的节点出发，能到达的节点"""
    # initial
    
    # level 1 
    connected = topology[x]
    
    
    # search for  level 2
    index_of_connected_1 = connected.nonzero()[0]
    connected_all = set()
    for i in index_of_connected_1:
        # print(i)
        connected = topology[i]
        index_of_connected = connected.nonzero()
        # print(index_of_connected)
        
        connected_all = connected_all.union(index_of_connected[0])
        
    return connected_all
        
        
def make_window_sample(alarms, win_size = 300, remove_outlier = True):
    """make window size"""
    alarms = alarms.sort_values(by='start_timestamp')
    alarms['win_id'] = alarms['start_timestamp'].map(lambda elem:int(elem/win_size))

    
    
    shape_alarm = alarms.shape
    
    # 去掉一些一个window内太多或者太少的
    if remove_outlier:
        max = alarms.groupby(['win_id'])['start_timestamp'].count().quantile(0.97)
    
    #太少的反而有很多的时候很关键，继续进行保留
    # min = alarms.groupby(['win_id'])['start_timestamp'].count().quantile(0.05)
    
    # alarms = alarms.groupby(['win_id']).filter(lambda x: len(x) < max and len(x) > min)
        alarms_for_apply = alarms.copy()
        alarms = alarms.groupby(['win_id']).filter(lambda x: len(x) < max )
    
        print("Window size {} Total {} removed {} alarms".format(win_size,
                                                                shape_alarm[0],
                                                                shape_alarm[0] - alarms.shape[0]))
        
    
    print("Window size {} Total {} alarms".format(win_size, alarms.shape[0]))
    
    samples=alarms.groupby(['alarm_id','win_id'])['start_timestamp'].count().unstack('alarm_id')
    samples = samples.dropna(how='all').fillna(0)
    samples = samples.sort_index(axis=1)
    
    return samples

def make_window_sample_multi(alarms, win_size = [450, 900, 1500], remove_outlier = True):
    """make window size"""

    # win_size = [450, 600, 900, 1200]
    
    s_list = []
    for w in win_size:
        s = make_window_sample(alarms, win_size = w, remove_outlier=remove_outlier)
        s_list.append(s)
    s_all = pd.concat(s_list)
    
    return s_all
        



def make_sample_based_on_topo(alarms, topology, win_size = [1000,1500], remove_outlier = True):
    """make window size"""
    
    samples_list = []
    
    device_count = topology.shape[0]
    
    for start in range(device_count):

        connected = start_with_x(topology, start)

        print("Looking for connected, Processing device: {} Number of Connected: {}".format(start, len(connected)))

        alarms_connected = alarms[alarms['device_id'].isin(connected)]

        print("Number of alarms connected: {} Percentage {:.2f}".format(alarms_connected.shape[0], alarms_connected.shape[0]/alarms.shape[0]))

        # window_sample = make_window_sample(alarms_connected, win_size=300)
        
        samples = make_window_sample_multi(alarms_connected, win_size=win_size, remove_outlier = remove_outlier)
        
        
        
        samples_list.append(samples)
        
    samples_all = pd.concat(samples_list)
    
    
    # 这里发现了na 先快速处理一下
    
    na_count = samples_all.isna().sum()
    print("NA count: {} Percentage {}".format(na_count, na_count/samples_all.shape[0]))
    
    samples_all = samples_all.fillna(0)
    
    return samples_all