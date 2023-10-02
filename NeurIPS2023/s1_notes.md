


# 参考信息


第一名的解决方案，对于dataset 4效果非常不好，但是对于其他的数据集效果非常好，可以作为一个baseline

https://codalab.lisn.upsaclay.fr/my/competition/submission/538031/detailed_results/

======= Set 1 (Dataset_1_graph_matrix): score(dataset_1_set1_score)=1.000000000000 =======
======= Set 2 (Dataset_2_graph_matrix): score(dataset_2_set1_score)=0.993333333333 =======
======= Set 3 (Dataset_3_graph_matrix): score(dataset_3_set1_score)=1.000000000000 =======
======= Set 4 (Dataset_4_graph_matrix): score(dataset_4_set1_score)=0.180722891566 =======
======= Avg_Score: 0.793514056225=======


第二名类似
https://codalab.lisn.upsaclay.fr/my/competition/submission/540357/detailed_results/
======= Set 1 (Dataset_1_graph_matrix): score(dataset_1_set1_score)=1.000000000000 =======
======= Set 2 (Dataset_2_graph_matrix): score(dataset_2_set1_score)=0.926666666667 =======
======= Set 3 (Dataset_3_graph_matrix): score(dataset_3_set1_score)=1.000000000000 =======
======= Set 4 (Dataset_4_graph_matrix): score(dataset_4_set1_score)=0.144578313253 =======
======= Avg_Score: 0.767811244980=======


后边的名次也是基本类似，核心的差距还是在前边的数据集上是不是可以表现比较好

https://codalab.lisn.upsaclay.fr/my/competition/submission/543479/detailed_results/

======= Set 1 (Dataset_1_graph_matrix): score(dataset_1_set1_score)=0.865979381443 =======
======= Set 2 (Dataset_2_graph_matrix): score(dataset_2_set1_score)=0.806666666667 =======
======= Set 3 (Dataset_3_graph_matrix): score(dataset_3_set1_score)=0.830769230769 =======
======= Set 4 (Dataset_4_graph_matrix): score(dataset_4_set1_score)=0.168674698795 =======
======= Avg_Score: 0.668022494419=======





# 第一次常识性的提醒

Window size 1000 使用较少的数据集进行

1，3 都使用了pc with prior
2，使用了notears with priori knowledge 得到了一定的分数
4使用了直接的PC



======= Set 1 (Dataset_1_graph_matrix): score(dataset_1_set1_score)=0.000000000000 =======
======= Set 2 (Dataset_2_graph_matrix): score(dataset_2_set1_score)=0.280000000000 =======
======= Set 3 (Dataset_3_graph_matrix): score(dataset_3_set1_score)=0.000000000000 =======
======= Set 4 (Dataset_4_graph_matrix): score(dataset_4_set1_score)=0.000000000000 =======
======= Avg_Score: 0.070000000000=======


# 数据集


预处理
1. 采用更多的window sizel类型 以及不同的window size来进行处理，改变长度进行 正在进行中
2. 有一些alert太过高频，进行去除?
3. window size过后 有一些就会太不好




# 第二次训练

dataset 3

预处理
多窗口 + 去除特别多+特别少的window

loss 基本5轮以后在129

感官上发现的一些causal，会更加的分散一些


TODO：尝试一下几轮的改变

还是继续一样不管dataset4先在其他的上达到比较好的分数
s2_1

完成了基本的pipeline可以大规模的跑单一的notears


在经过一些纯粹数据的处理以后，1-3dataset 已经达到了0.3左右的分数
dataset 2 分数依然是0.28


======= Set 1 (Dataset_1_graph_matrix): score(dataset_1_set1_score)=0.278350515464 =======
======= Set 2 (Dataset_2_graph_matrix): score(dataset_2_set1_score)=0.280000000000 =======
======= Set 3 (Dataset_3_graph_matrix): score(dataset_3_set1_score)=0.353846153846 =======
======= Set 4 (Dataset_4_graph_matrix): score(dataset_4_set1_score)=0.000000000000 =======
======= Avg_Score: 0.228049167328=======


TODO：(等第三种方案结束再进行)
在这里单纯的换一个方法，看一下换一个方法是不是会有更好，以决定后续是不是继续用notears
1. 考虑DECI
2. 继续考虑传统的方法6


# 第三次训练  S3  0 分

S3最终选择先试一下GOLEM的速度

GOLEM 5000 iter的时候还是速度ok
最终还是报错了

最终得到了0分

(这里也再调整了window size， 从300,600,900,1200，调整到了  450,900两个点，也会有一些影响)
再试一下训练的方法问题

Start fitting dataset_2 Shape of samples: (1810, 49)
Start fitting dataset_1 Shape of samples: (1813, 39)
Start fitting dataset_3 Shape of samples: (1814, 31)

第二次fit的时候还好 没有出现错误，完整跑完了5000 iter
2023-10-01 17:40:22,222 - /Users/zhitaogao/opt/anaconda3/envs/gcastle/lib/python3.9/site-packages/castle/algorithms/gradient/notears/torch/golem.py[line:220] - INFO: [Iter 5000] score=299.391, likelihood=295.982, h=3.2e-02

但是最终的结果是完全一致的，算法没有问题。
继续retry2的时候重新看一下window size，继续放大，并且执行更多iter

Start fitting dataset_2 Shape of samples: (2173, 49)
Start fitting dataset_1 Shape of samples: (2176, 39)
Window size 1500 Total 198962 removed 39070 alarms
Start fitting dataset_3 Shape of samples: (2177, 31)


Retry 3 的时候 还是有一些区别的

diff of dataset 0: 113
diff of dataset 1: 106
diff of dataset 2: 70
diff of dataset 3: 0

依然还是0分
对比一下和之前的sub2 还是有一些差距


# S4

继续看一下预处理的部分的可能性，还是继续再回到notears

TODO的一个想法: 基于Topylogy每次制作windows的时候，都保证有topology的存在，如果没有topology的部分就进行去掉
1. 先随机寻找大量topology的组合。如果没有topology的关系，避免构建相关的数据集影响结果
2. 在每一种组合上构建数据集
3. 构建（组合+组合）*（组合+组合）类似大数据集
3. 在组合上进行notears学习，学到10-100个结果
4. 最终进行一轮融合投票决定最后的因果关系



Toplogy的组合的数量是非常大的，没有发现明显的子网络，这个思路放弃。
(能发现到从任何一个地方开始，到两层基本就是覆盖了全部了)


数量级很大
Method notears Start fitting dataset_3 Shape of samples: (94458, 31)





(后续需要跟进，一些tricks的想法，如果topology链接上显示内容很少，那么因果关系就是不明确的，可以考虑去除这种情况)（还没想清楚）


9.30 方案3这个不继续跟进了

# 第四次或者

找一个更稳定需要时间更少的方法
TTPM，CGNN，SAM，GES等方法。先从GES开始



## 预处理的部分

9/30 不同的设备，不是都有所有的报警。


预处理1：设备归类
1. 有些很明显的pattern，有设备类型的集中。
1. 需要对这些设备进行归类，归类以后进行处理。(已经完成归类，)
1. （对这些归类的设备进行正则化处理），同时我们假设出现太多同样一种报警的设备，进行去掉（这个在前边一步已经完成了）
1. 把所有相同类型的设备的信息进行单独的聚合形成样本，然后进行处理。比如抽取单独的设备类型1，然后再去形成window
1. 是不是有？


只用相同的数据集进行建模


s_1_3_preprocessing


预处理2：拓扑结构数据集

一些更多的思考
1. 对于大量的报警数量的报警，进行一些相应的log计算，正则化






方法对比的部分



1. Notears，可以包含priori
2. PC，可以包含priori
1. GOLEM 比较慢
3. GES 模式参数也还是非常的慢
4. 






# 更多最终的tricks

一个最终处理的方式：
从学到的graph_matrix里边，去掉完全没有topology的部分。这个地方看过以后发现还是不存在的。几乎任何两个链接都可以存在因果关系

