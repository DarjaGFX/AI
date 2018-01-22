import numpy as np

def k_means (data, n, weight = None):
    data = np.array(data)
    ### normalizing Data
    for i in range(0, len(data[0][:])):
        min_d = np.amin(data, axis=0)
        max_d = np.amax(data, axis=0)

    for j in range (0, len(data[0][:])):
        for i in range(0, len(data[:][0])-1):
            data[i][j] = (data[i][j] - min_d[j] ) / ( max_d[j] - min_d[j] )
    #### END ####

    if weight == None:
        weight = np.ones(len(data[0, :]))
    prevRes = None
    lastRes = None
    while True:
        if n>len(data[:,0]):
            print('Desired Cluster Number is Greater than Data Entries ')
            return
        dataTable = []      # dataTable[i] = j     ==>  data[i,:] is in cluster j

        if lastRes == None:
            cb = []             # codebook , Select n sample data as mean of each cluster
            for i in range(n):
                cb.append(data[len(data[:, 0])-i-1])
        else:
            cb = lastRes

        for i in range(len(data[:, 0])):
            distances = []  # distance between Data[i,:] and each CodeBooks
            for j in range(n):
                dataTemp = np.array(data)
                cbTemp = np.array(cb)
                distances.append(np.sqrt(np.sum(weight[:]*((dataTemp[i, :]-cbTemp[j, :])**2))))
            dataTable.append(np.argmin(distances))

        ### START updating CodeBook###
        for j in range(n):
            count_cluster_j = 0
            feature_sum_clstr_i = np.zeros(len(data[0, :]))
            for i in range(len(dataTable)):
                    if dataTable[i] == j:
                        count_cluster_j += 1
                        for k in range(len(data[0, :])):
                            feature_sum_clstr_i[k] += data[i, k]
            cb[j] = feature_sum_clstr_i/count_cluster_j
        ### END ###

        lastRes = cb
            
        if lastRes is prevRes:
            break
        else:
            prevRes = lastRes
    return lastRes
