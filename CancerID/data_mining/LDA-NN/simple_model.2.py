from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.models import load_model
from keras.utils.np_utils import to_categorical

from keras import metrics
import keras
import pandas as pd
import numpy as np

dis = pd.read_csv('./data/p_dis.csv')
dis = dis.values

d_c = np.load("./data/d_topic.npy")

x_train = d_c
y_train = dis[:4847,:]
x_test = np.load("./data/test_doc_topic_distribution.npy")
y_test = dis[4847:,:]

model = Sequential()
model = load_model('./model/simple.json')
# get_3rd_layer_output = K.function([model.layers[0].input, K.learning_phase()],
                                #   [model.layers[3].output])
# output in test mode = 0
# layer_output = get_3rd_layer_output([x_test, 0])[ 0]

# print layer_output
new_model = Sequential()
for layer in model.layers[:-2]:
    new_model.add(layer)
    print('new_model.layers', len(new_model.layers))
    print(new_model.layers)

new_model.add(Dense(416))
new_model.compile(loss='mean_squared_error',
            optimizer='adam',
            metrics = ['accuracy'])


# model.save('./model/simple.json')
# model.save_weights('./model/simple.h5')

result = new_model.predict(x_test,batch_size=20)
print(result)
# np.save('./result/simple_result.npy',result)
# # score = model.evaluate(x_test, y_test, batch_size=128)

# print
# print score
