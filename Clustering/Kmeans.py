import numpy as np
import random

def distance(x,y,algorithm = "Euclidean" , weight = None):
    """
     calc distance between x,y 
     \neach feature of `X` can have it's own `weight` of priority!
    """
    if weight is None:
        weight = np.ones(len(x))
    if algorithm is "Euclidean":
        return Euclidean(x,y,weight=weight)

def Euclidean(x,y , weight = None):
    """
     returns Euclidean distance between `X` and `Y` 
    \neach feature of `X` can have it's own `weight` of priority!
    """
    if weight is None:
        weight = np.ones(len(x))
    x = np.array(x)
    y = np.array(y)
    return np.sqrt(np.sum(weight*((x-y)**2)))

def k_means (data, n, weight = None):
    """
        returns `centroids`,`classes`,`clusters`.
        \nfinds `n` nodes as center of `n` Clusters for Data.
        \neach feature of `data` can has its own `weight`.
        \n`data` must be in following format:
        \n`data` = [
        [data1_feature1 , data1_feature2 , ... data1_featureM],
        [data2_feature1 , data2_feature2 , ... data2_featureM],
        .
        .
        .
        [dataN_feature1 , dataN_feature2 , ... dataN_featureM]
        ]
    """
    data = np.array(data)
    realData = data
    ### normalizing Data
    min_d = np.amin(data, axis=0)
    max_d = np.amax(data, axis=0)

    totalmin = np.amin(min_d, axis=0)
    totalmax = np.amax(max_d, axis=0)
    data = (data - min_d ) / ( max_d - min_d )
    #### END ####
    min_mind = int(np.amin(np.amin(data, axis=0), axis=0))
    max_maxd = int(np.amax(np.amax(data, axis=0), axis=0))
    start = [min_mind,min_mind]
    end = [max_maxd,max_maxd]
    meanWidth = distance(start,end)/n

    if weight == None:
        weight = np.ones(len(data[0, :]))
    prevRes = None
    lastRes = None
    while True:
        if n>len(data[:,0]):
            print('Desired Cluster Number is Greater than Data Entries ')
            return
        dataTable = []      # dataTable[i] = j     ==>  data[i,:] is in cluster j

        ###
        ### Select n sample as center of clusters , each sample has len(data[0,:]) features!!
        ### (first time codebook)
        if lastRes == None:
            cb = []             # codebook , (centroids)
            for i in range(n):
                tmparr = np.zeros(len(data[0,:]))    # temp array to save temporarily a centroid till set all its features a value!
                for f in range(len(data[0,:])):
                    dist = np.zeros(n)
                    tmparr[f] = random.uniform(i*meanWidth,(i+1)*meanWidth)
                cb.append(tmparr)
        else:
            cb = lastRes
        ### END ###

        for i in range(len(data[:, 0])):
            distances = []  # distance between Data[i,:] and each CodeBooks
            for j in range(n):
                dataTemp = np.array(data)
                cbTemp = np.array(cb)
                distances.append(distance(dataTemp[i, :],cbTemp[j, :],algorithm= "Euclidean" ,weight=weight))
            dataTable.append(np.argmin(distances))

        ### START updating CodeBook###
        for j in range(n):
            count_cluster_j = 0
            feature_sum_clstr_i = np.zeros(len(data[0, :]))
            for i in range(len(dataTable)):
                    if dataTable[i] == j:
                        count_cluster_j += 1
                        feature_sum_clstr_i += data[i,:]
            cb[j] = feature_sum_clstr_i/count_cluster_j
        ### END ###
        lastRes = cb

        if lastRes == prevRes:
            break
        else:
            prevRes = lastRes

    ###
    ### back to normal range
    ###
    lastRes = lastRes*(max_d-min_d)
    lastRes += min_d
    ###END###
    centroids = lastRes
    classes = dataTable
    Clusters = []
    for i in range(n):
        tmp = []
        for j in range(len(data)):
            if classes[j]==i:
                tmp.append(realDatadata[j,:])
        Clusters.append(tmp)

    return centroids,classes,Clusters