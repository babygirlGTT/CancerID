'''
Used to generate P R F of model1
Change file path to generate data for model2
'''
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

diagnose_result = np.load('../result/simple_result.npy')
lenth = diagnose_result.shape[0]

real_disease_matrix = pd.read_csv('../data/p_dis.csv')
test_patient = real_disease_matrix.iloc[4847:,:]

def recall(n):
    recall_sum = 0
    # recall_list = []
    real_set = set([])
    for i in range(lenth):
        real = set(int(r_d) for r_d in test_patient.iloc[i,:][test_patient.iloc[i,:] == 1].index)
        pred = np.argsort(diagnose_result[i,:])[::-1]
        denominator = len(real)
        numerator = 0.0
        for item in pred[:n]:
            if item in real:
                numerator += 1
        recall = numerator/denominator
        # find best performance
        if n == 5 and recall == 1:
            print(i,real)
        #     for iii in real:
        #         real_set.add(iii)

        # recall_list.append(recall)
        recall_sum += recall
    # recall_list.sort()
    # plt.plot(recall_list[::-1])
    # plt.grid()
    # plt.show()
    return recall_sum/lenth

def precision(n):
    precision_sum = 0.0
    # precision_list = []
    for i in range(lenth):
        real = set(int(r_d) for r_d in test_patient.iloc[i,:][test_patient.iloc[i,:] == 1].index)
        pred = np.argsort(diagnose_result[i,:])[::-1]
        count = 0
        for item in pred[:n]:
            if item in real:
                count += 1
                break
        # precision_list.append(count)
        precision_sum += count

    return precision_sum/lenth
# precision_list.sort()
# plt.plot(precision_list[::-1])
# plt.show()
precision_list = []
recall_list = []
f1_list = []

for i in range(45):
    newi = i+5 
    print(newi)
    P = precision(newi)
    precision_list.append(P)
    R = recall(newi)
    recall_list.append(R)
    f1_list.append(2 * P * R/(P + R))

np.save('./simple_Precision.npy',np.array(precision_list))
np.save('./simple_Recall.npy',np.array(recall_list))
np.save('./simple_F1.npy',np.array(f1_list))

xs = np.arange(45) + 5
p = plt.plot(xs, precision_list,color='r')
r = plt.plot(xs, recall_list,color='y') 
f = plt.plot(xs, f1_list)

plt.xlabel("Number of K")
plt.ylabel("Value")
plt.grid()
plt.legend((p[0],r[0],f[0]),('precision','recall','f1'))
plt.show()