import tlsh
import json
import numpy as np
# from sklearn.neighbors import KDTree
import random


    # for filename, hash_value in tlsh_dict.items():
    #     print(f"Giá trị TLSH của tệp tin {filename}: {hash_value}")
with open('tlsh1.json', 'r') as f:
        tlsh_dict = json.load(f)
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
    return len(N.data)<=101

def closestItem(N, S):
    # myDict = N.lc.copy()
    # myDict = N.lc.update(N.rc)
    closest = (None, float('inf'))
    for file, hashval in N.data.items():
        if file != list(S.keys())[0]:
            dist = tlsh.diff(hashval , S[list(S.keys())[0]])
            if dist < closest[1]:
                closest = (file, dist)


    return closest

def Dist(X, S):
    return tlsh.diff(list(X.values())[0],list(S.values())[0])
def Search(N, S):


    if isLeaf(N):
        X , d = closestItem(N, S)
        return (X,d)
    else:
        thisDist = Dist(N.split, S)
        
        if thisDist <= N.threshold:
            return Search(N.lc, S)
        else:
            return Search(N.rc, S)
def main():
    S = {'00a2924222061bb2814f1ba9dfec8164': 'T120C45D3CABAC0379D073813CC5A88132FA7274682B2196CF51A4913D5E2FEF46A79B51'}
    
    # N1 = Node(tlsh_dict , split=None, threshold=None, lc=None, rc=None )
    # K = TreeBuild(N1 , 2)
    # K1 = Search(K, S)
    # print(K1)
    CDist = 1000
    tlsh_dict_test = dict(list(tlsh_dict.items())[:1000])
    print(HAC_T(tlsh_dict , CDist))

    
# def HAC_T(D, CDist):
#     node_root = Node(data=tlsh_dict)
#     toot = TreeBuild(node_root, 3)
def HAC_T(D, CDist):
    # Step 1: Preprocess data
    ListPair = {}
    for d in range(CDist+1):
        ListPair[d] = []
    N1 = Node(D, split=None, threshold=None, lc=None, rc=None)
    root = TreeBuild(N1, 100)

    for A in D.items():
        dict_A = {A[0]: A[1]}
        myroot = root
        (B, d) = Search(myroot, dict_A)
        if d < CDist:
            ListPair[d].append((A[0],B))

    # Step 2: Cluster data
    clusters = {}
    for A in D.items():
        clusters[A[0]] = set([A[0]])

    for d in range(CDist+1):
        for (X1,X2) in ListPair[d]:
            if clusters[X1] != clusters[X2]:
                clusters[X1].update(clusters[X2])
                for item in clusters[X2]:
                    clusters[item] = clusters[X1]

    num_clusters = len(set([tuple(sorted(items)) for items in clusters.values()]))
    print(num_clusters)
    # Return the final clusters
    return list[set([tuple(sorted(items)) for items in clusters.values()])]

if __name__ == '__main__':
    main()
