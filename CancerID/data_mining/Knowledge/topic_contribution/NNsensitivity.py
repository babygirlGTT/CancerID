'''
Calculate sensitivity
Generate topic contribution to 7 diseases
'''
import json
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense, Dropout, Activation
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
real_disease_matrix = pd.read_csv('../data/p_dis.csv')
model = Sequential()

model = load_model('../model/simple.json')  
model.load_weights("../model/simple.h5")
weighs = model.get_weights()
train_data = np.load('../data/d_topic.npy')
test_data = np.load('../data/test_doc_topic_distribution.npy')
data = np.concatenate((train_data,test_data))
support_dict={}
X = np.array([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1.5])
for index in range(20):
    X[index] = 1.5
    X[index-1] = 1
    transformed_data = data * X
    result1 = model.predict(data)
    result2 = model.predict(transformed_data)
    for i in range(data.shape[0]):
        real = [int(r_d) for r_d in real_disease_matrix.iloc[i,:][real_disease_matrix.iloc[i,:] == 1].index]
        for real_item in real:
            rate = (result2[i,:][real_item]-result1[i,:][real_item])/result1[i,:][real_item]
            if real_item not in support_dict:
                support_dict[real_item] = {str(index):[rate]}
            elif index not in support_dict[real_item]:
                support_dict[real_item][str(index)] = [rate] 
            else:
                support_dict[real_item][str(index)].append(rate)
for disease, dict1 in support_dict.items():
    for topic, prob in dict1.items():
        fullnumber = np.mean(dict1[topic])
        dict1[topic] = '%.5g'%fullnumber

output = open('new_support_dict.pkl', 'wb')
pickle.dump(support_dict, output)
output.close()

# plt.plot(result1[0,:])
# plt.plot(result2[0,:],color='r')
# plt.show()
