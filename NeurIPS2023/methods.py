# end to end methods

import pandas as pd
import plotly.express as px


import pandas as pd

from castle.algorithms import PC
from castle.algorithms import Notears,GES
from castle.algorithms import GOLEM,RL

from toolkit import save_result

import importlib
import preprocess
importlib.reload(preprocess)
from preprocess import *

import multiprocessing as mp



class Causal():
    
    
    def __init__(self,
                 x, 
                 y = None,
                 prior_knowledge=None,
                 method='notears',
                 **kwargs):
        self.x = x
        self.y = y
        self.prior_knowledge = prior_knowledge
        self.method = method
        self.estimated = None
        self.kwargs = kwargs
        # extra parameters for different methods
        self.max_iter = kwargs.get('max_iter', 100)
        
    
    def fit_no_tears(self, including_prior_knowledge=True):
        
        nt = Notears(max_iter=self.max_iter,
                     # loss nan
                     loss_type='logistic',
                     )
        if including_prior_knowledge:
            nt.learn(self.x, 
                     prior_knowledge = self.prior_knowledge,
                     max_iter = self.max_iter)
            
            self.estimated = nt.causal_matrix
    
    
    def fit_GOLEM(self,including_prior_knowledge=True):
        
        
        # 5000 as a baseline
        golem = GOLEM(num_iter = 10000)
        if including_prior_knowledge:
            golem.learn(self.x, 
                        prior_knowledge = self.prior_knowledge,
                        # max_iter = self.max_iter
                        )
            
            self.estimated = golem.causal_matrix
    
    def fit_GES(self):
        
        ges = GES()
        ges.learn(self.x, 
                    prior_knowledge = self.prior_knowledge,
                    max_iter = self.max_iter)
        
        self.estimated = ges.causal_matrix
        
    def fit_pc(self):
        
        pc = PC()
        pc.learn(self.x)
        self.estimated = pc.causal_matrix
        

    def fit(self, data, method='notears'):
        
        if method == 'notears':
            self.fit_no_tears()
        
        return self.estimated            




# 一个方法可以迅速的计算多个数据集


import threading
import datetime

# def causal_pipeline(data, method = 'notears', solution_name = 2, preprocessed = False):
def causal_pipeline(kwargs):
    
    # print("args", *args)
    print("Get kwargs in causal pipeline: ", kwargs)
    
    data = kwargs.get('data', None)
    method = kwargs.get('method', 'notears')
    solution_name = kwargs.get('solution_name', 2)
    preprocessed = kwargs.get('preprocessed', False)
    
    print("Start causal_pipeline dataset {} with method {}, solution name {} preprocessed {}".format(data[0], method, solution_name, preprocessed))
    
    data_name, alarms, causal_prior, topology, rca_prior, prior_knowledge =\
    data[0], data[1], data[2], data[3], data[4], data[5]
    
    # pre-process
    
    
    # S4 基于topo的预处理，量会很大
    if not preprocessed:
        print("Pre Processing dataset {}".format(data_name))

        samples = make_sample_based_on_topo(alarms, topology)
        # samples = make_window_sample_multi(alarms)

    # 处理过的在最后一个
    if preprocessed:
        samples = data[6]
        
        
        # 临时看一下sample以后会不会有问题
    
    
    # samples = samples.sample(1000)
    
    
    
    print("Method {} Start fitting {} Shape of samples: {}".format(method, data_name, samples.shape))
    c = Causal(samples, prior_knowledge=prior_knowledge)
    
    if method == 'notears':
        c.fit_no_tears()
    if method == 'golem':
        c.fit_GOLEM()
    if method == 'ges':
        c.fit_GES()
    
    est = c.estimated
    
    # save
    
    date_time_str = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    solution_name = date_time_str + '-' +str(solution_name)
    
    save_result(est, dataset=data_name, solution = solution_name)
    print("Saved solution 2 for dataset 1 to ./submission/solution2/1_graph_matrix.npy")
    




def causal_all(func = causal_pipeline, list_of_dataset = None, preprocessed = False):
    

    # # multi-process
    # for data in list_of_dataset:
        
    #     threads = []
    #     t = threading.Thread(target=causal_pipeline, args=(data,preprocessed))
    #     threads.append(t)
    #     t.start()
        
    # # wait for all threads to finish
    # t.join()
    
    print("All dataset processed")
    
    
#    multi processing version


    jobs = []
    
    for data in list_of_dataset:
        
        args= {'data':data, 'method':'notears', 'solution_name':2, 'preprocessed':preprocessed}
        
        p = mp.Process(target=func, args=(args,)) 
        jobs.append(p)
        p.start()
        
    for proc in jobs:
        proc.join()

    print("All dataset processed")



