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

model.add(Dense(512, activation='relu', input_dim=20))
model.add(Dropout(0.5))
model.add(Dense(256, activation='relu'))
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

model.save('./model/simple.json')
model.save_weights('./model/simple.h5')

result = model.predict(x_test,batch_size=20)
np.save('./result/simple_result.npy',result)
# score = model.evaluate(x_test, y_test, batch_size=128)

print
print(score)
