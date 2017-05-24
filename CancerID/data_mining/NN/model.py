import tensorflow as tf
import numpy as np
import pandas as pd

tf.logging.set_verbosity(tf.logging.INFO)

def main():

    COLUMNS = ["topic1","topic2","topic3","topic4","topic5","topic6","topic7","topic8",
               "topic9","topic10","topic11","topic12","topic13","topic14","topic15","topic16",
               "topic17","topic18","topic19","topic20"]

    feature_data = np.load('d_topic.npy')
    label_data = np.load('doc_dis.npy')

    feature_columns = [tf.contrib.layers.real_valued_column(k) for k in COLUMNS]
  # Build 3 layer DNN with 10, 20, 10 units respectively.
    classifier = tf.contrib.learn.DNNRegressor(feature_columns=feature_columns,
                                              hidden_units=[10, 20, 10],
                                              label_dimension=2020,
                                              model_dir="/tmp/disease_model")
  # Input builders
    def input_fn_train(feature, label):
        feature_tensor = {k: tf.constant(feature[:750,i]) for i,k in enumerate(COLUMNS)}
        label_tensor = tf.constant(label[:750,:])
        return feature_tensor, label_tensor

   # Fit model.
    classifier.fit(input_fn=lambda: input_fn_train(feature_data, label_data), steps=1000)

    def input_fn_eval(feature, label):
        feature_tensor = {k: tf.constant(feature[750:,i]) for i,k in enumerate(COLUMNS)}
        label_tensor = tf.constant(label[750:,:])
        return feature_tensor, label_tensor

#   # Evaluate accuracy.
#     accuracy_score = classifier.evaluate(input_fn=lambda: input_fn_eval(feature_data, label_data),
#                                        steps=1)["accuracy"]

#     print("\nTest Accuracy: {0:f}\n".format(accuracy_score))

#   # Classify two new flower samples.
#   def new_samples():
#     return np.array(
#       [[6.4, 3.2, 4.5, 1.5],
#        [5.8, 3.1, 5.0, 1.7]], dtype=np.float32)

    predictions = list(classifier.predict(input_fn=lambda: input_fn_eval(feature_data, label_data)))
    print("New Samples, Class Predictions:    {}\n".format(predictions))

if __name__ == "__main__":
    main()