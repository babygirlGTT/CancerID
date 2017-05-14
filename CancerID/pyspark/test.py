from pyspark.ml.feature import CountVectorizer
from pyspark import SparkConf, SparkContext, StorageLevel
from pyspark.mllib.linalg import SparseVector
from pyspark.mllib.regression import LabeledPoint

sc = SparkContext()
# Create a labeled point with a positive label and a dense feature vector.
pos = LabeledPoint(1.0, [1.0, 0.0, 3.0])
print pos
# Create a labeled point with a negative label and a sparse feature vector.
neg = LabeledPoint(0.0, SparseVector(3, [0, 2], [1.0, 3.0]))
print neg
# Input data: Each row is a bag of words with a ID.
file_rdd = sc.textFile("./text.txt")
print file_rdd
# fit a CountVectorizerModel from the corpus.
# cv = CountVectorizer(inputCol="words", outputCol="features", vocabSize=3, minDF=2.0)
# model = cv.fit(df)
# result = model.transform(df)
# result.show()