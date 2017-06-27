from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.utils.np_utils import to_categorical
from sklearn.grid_search import GridSearchCV
from keras.wrappers.scikit_learn import KerasClassifier

from keras import metrics
import keras
import pandas as pd
import numpy as np

dis = pd.read_csv('./data/p_dis.csv')
dis = dis.values

training_doc = np.load("./data/d_topic.npy")
testing_doc = np.load("./data/test_doc_topic_distribution.npy")
data = np.concatenate([training_doc,testing_doc])
shuffle_number = np.arange(data.shape[0])
np.random.shuffle(shuffle_number)

x_train = data[shuffle_number][:4847,:]
y_train = dis[shuffle_number][:4847,:]
x_test = data[shuffle_number][4847:,:]
y_test = dis[shuffle_number][4847:,:]

# def create_model():

#     model = Sequential()
#     model.add(Dense(512, activation='relu', input_dim=20, kernel_initializer='glorot_uniform'))
#     model.add(Dropout(0.5))
#     model.add(Dense(256, activation='relu',kernel_initializer='glorot_uniform'))
#     model.add(Dropout(0.5))
#     model.add(Dense(416, activation='softmax'))

#     model.compile(loss='categorical_crossentropy',
#                 optimizer='adam',
#                 metrics=["accuracy", metrics.categorical_accuracy])
#     return model
# to_callback = keras.callbacks.TensorBoard(log_dir='./Graph', histogram_freq=0,  
#           write_graph=True, write_images=True)


# model = KerasClassifier(build_fn=create_model, verbose=0)

model = Sequential()
model.add(Dense(512, activation='relu', input_dim=20, kernel_initializer='glorot_uniform'))
model.add(Dropout(0.5))
model.add(Dense(256, activation='relu',kernel_initializer='glorot_uniform'))
model.add(Dropout(0.5))
model.add(Dense(416, activation='softmax'))
model.compile(loss='categorical_crossentropy',
                optimizer='adam',
                metrics = ['accuracy',metrics.categorical_accuracy])

# batch_size = [20, 40, 60]
# epochs = [10,20,30,40,50]
# param_grid = dict(batch_size=batch_size, nb_epoch=epochs)
# grid = GridSearchCV(estimator=model, param_grid=param_grid, n_jobs=-1)
# grid_result = grid.fit(x_train, y_train)
# summarize results
# print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
# for params, mean_score, scores in grid_result.grid_scores_:
#     print("%f (%f) with: %r" % (scores.mean(), scores.std(), params))
model.fit(x_train, y_train,
           epochs=50,
           batch_size=20,
#         #   callbacks=[to_callback])
           validation_data=(x_test, y_test))

# model.save('./model/simple.json')
# model.save_weights('./model/simple.h5')

result = model.predict(x_test,batch_size=20)
np.save('./result/shuffle_result.npy',result)
# # score = model.evaluate(x_test, y_test, batch_size=128)

# print
# print score
