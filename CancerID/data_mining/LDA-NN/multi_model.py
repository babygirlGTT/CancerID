from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras import metrics
import keras.backend as K
from keras.utils.np_utils import to_categorical
from keras.wrappers.scikit_learn import KerasClassifier
import pandas as pd

import keras

import numpy as np

def top_5_acc(y_true, y_pred):
    return K.mean(K.in_top_k(y_pred, K.argmax(y_true, axis=-1), 5), axis=-1)


dis = pd.read_csv('./data/p_dis_comb.csv',header=None)
dis = dis.values

dis = keras.utils.to_categorical(dis)

d_c = np.load("./data/d_topic.npy")

x_train = d_c
y_train = dis[:4847,:]

x_test = np.load("./data/test_doc_topic_distribution.npy")
y_test = dis[4847:,:]

model = Sequential()
model.add(Dense(512, activation='relu', input_dim=20))
model.add(Dropout(0.8))
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.8))
model.add(Dense(1561, activation='softmax'))


model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy',top_5_acc])

model.fit(x_train, y_train,
          epochs=30,
          batch_size=128)
model.save('./model/multi.model')
model.save_weights('./model/multi.weigh')
result = model.predict(x_test,batch_size=128)

np.save('./result/multi_result.npy',result)
score = model.evaluate(x_test, y_test, batch_size=128)
print
print(score)
