# 这个算法的算法 3, 文件是针对 paper 2 Global reliable diagnosis of networks based on Self-Comparative Diagnosis Model and g-good-neighbor property

import random
from utils.MLEC import MLEC


def paper2(network, algo_return_H_num, l): 
    cur_return_H_num = 0
    good_H_list = []

    for node in network.H:
        if p2_algo3(network, node, l):
            good_H_list.append(node)
            cur_return_H_num += 1
            if cur_return_H_num >= algo_return_H_num:
                break

    return good_H_list


def p2_algo3(network, node, l):

    #FP 一直是 0 猜测算法哪里有错?2023年07月09日01:44:34,10000 的次数都不会出现超过 5 次,感觉有点奇怪
    Nad = Ndad = 0
    S = []
    if len(node.neighbors[0]) < network.g_goodN: #因为 H 网络节点的好邻居只存在于 H 网络中, 所以goodN 是只能 H;
        node.status = 1
        node.dec_level = -1
        return False
    
    uu = MLEC(node, node)
    nei_list = node.neighbors[0] + node.neighbors[1]
    for nei_node_id in nei_list:
        u_nei = MLEC(node, network.all_node[nei_node_id])
        if cal_SE(node, uu, u_nei, l) == l:
            # 说明检测没有问题
            Nad += 1
            S.append(network.all_node[nei_node_id])

    if Nad < network.g_goodN:
        node.status = 1
        node.dec_level = -1
        if node.level == 0:
            print("Nad < g_goodN")
        return False
    
    for nei_node in S:
        nei_nei = MLEC(nei_node, nei_node)
        nei_u = MLEC(nei_node, node)
        mid_res = cal_SE(node, nei_nei, nei_u, l)
        if  mid_res < l:
            Ndad += 1

    if Ndad ==0:
        node.status = 1
        node.dec_level = 0
        return True
    else:
        node.status = 1
        node.dec_level = -1
        return False


def cal_SE(node, level1, level2, l):
    # 计算返回结果的相似度
    # 这里的 node 就是 w

    # 如果 node 是坏点, 那么 cal_SE 随机返回的是 1~l, 返回的是 l
    # 

    if node.level != 0:
        return random.randint(1, l)
        # 是坏点就随机返回
    
    if level1 == level2:
        return l
    else:
        return l - level2
    


# w 是个坏点，SE 结果随机值—1~l；不管 xi

# w 是个好点，rr(ww)
# — xi 是个好点：SE 是真实结果， = l
# — xi 是个坏点：SE < l

# 如果 w 和 xi，=l-1, SE 随机的？

# 但凡 w 是个坏点；也可能是 1~l-1