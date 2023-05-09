import tlsh
import json
import numpy as np
from sklearn.neighbors import KDTree
import random

S = {'00a2924222061bb2814f1ba9dfec8164': 'T120C45D3CABAC0379D073813CC5A88132FA7274682B2196CF51A4913D5E2FEF46A79B51'}

with open('tlsh.json', 'r') as f:
    tlsh_dict = json.load(f)
    # for filename, hash_value in tlsh_dict.items():
    #     print(f"Giá trị TLSH của tệp tin {filename}: {hash_value}")
    
class Node:
    def __init__(self,data = None ,  split=None, threshold=None, lc=None, rc=None):
        self.data = data
        self.split = split
        self.threshold = threshold
        self.lc = lc
        self.rc = rc
def SplitMethod(N, nitemsInLeaf):
    # Get the number of items in N
    nitems = len(N.data)

    # If the number of items is less than nitemsInLeaf, return NULL
    if nitems <= nitemsInLeaf:
        return None

    # Choose a random element from N
    Y_key, Y_hash = random.choice(list(N.data.items()))
    Y = {Y_key : Y_hash}

    # print(Y_key)
    # Calculate TLSH diffs between Y and other nodes
    diffs = []
    for xi_key, xi_hash in N.data.items():
        if xi_key != Y_key:
            diffs.append(tlsh.diff(Y_hash, xi_hash))
    diffs.sort()
    # print(diffs)

    # Choose the median of the TLSH diffs as the threshold T
    
    if len(diffs) == 2:
      T = sum(diffs) / 2
    else:
      T = diffs[len(diffs) // 2]
      # print(T)
    
    # Partition data into X1 and X2 based on T
    X1 = {xi_key: xi_hash for xi_key, xi_hash in N.data.items() if xi_key != Y_key and tlsh.diff(Y_hash, xi_hash) <= T}
    X2 = {xi_key: xi_hash for xi_key, xi_hash in N.data.items() if tlsh.diff(Y_hash, xi_hash) > T}

    return (Y, T, X1, X2)
N1 = Node(tlsh_dict , split=None, threshold=None, lc=None, rc=None )

def TreeBuild(N, nitemsInLeaf  ):
    # Split N into Y, T, X1, X2
    res = SplitMethod(N, nitemsInLeaf)
    
    if res is not None:
        Y, T, X1, X2 = res
        N.split = Y
        N.threshold = T
        N.lc = Node(X1 , split=None, threshold=None, lc=None, rc=None )
        TreeBuild(N.lc, nitemsInLeaf)
        N.rc = Node(X2 , split=None, threshold=None, lc=None, rc=None)
        TreeBuild(N.rc, nitemsInLeaf)
        
    return N
K = TreeBuild(N1 , 2)
def print_tree(node):
    if node is not None:
        print(node.data)
        print('do dai cua node: ' , len(node.data))
        # print('node trai: ')
        # print(node.rc.data)
        # print('node phai: ')
        # print(node.lc.data)
        print_tree(node.rc)
        print_tree(node.lc)
# print_tree(K)
def isLeaf(N):
    return len(N)<=3 

def closestItem(N, S):
    # myDict = N.lc.copy()
    # myDict = N.lc.update(N.rc)
    closest = (None, float('inf'))
    for file, hashval in N.items():
        dist = tlsh.diff(hashval , S[list(S.keys())[0]])
        if dist < closest[1]:
            closest = (file, dist)


    return closest

def Dist(X, S):
    return tlsh.diff(list(X.values())[0],list(S.values())[0])
def Search(N, S):
    data = N.data
    # print('data: ' , data)
    if isLeaf(data):
        X , d = closestItem(data, S)
        return (X,d)
    else:
        thisDist = Dist(N.split, S)
        
        if thisDist <= N.threshold:
            return Search(N.lc, S)
        else:
            return Search(N.rc, S)
K1 = Search(K, S)

print(K)
