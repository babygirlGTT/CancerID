import numpy as np 
import matplotlib.pyplot as plt
m_p = np.load("multi_Precision.npy")
m_r = np.load("multi_Recall.npy")
m_f = np.load("multi_F1.npy")
s_p = np.load("simple_Precision.npy")
s_r = np.load("simple_Recall.npy")
s_f = np.load("simple_F1.npy")

xs = np.arange(45) + 5
mp = plt.plot(xs, m_p,color='g')
mr = plt.plot(xs, m_r,color='darkred') 
mf = plt.plot(xs, m_f,color='orange')
sp = plt.plot(xs, s_p,color='lime')
sr = plt.plot(xs, s_r,color='red') 
sf = plt.plot(xs, s_f,color='yellow')

plt.xlabel("Number of K")
plt.ylabel("Value")
plt.grid()

plt.legend((mp[0],mr[0],mf[0],sp[0],sr[0],sf[0]),('model1_precision','model1_recall','model1_f1','model2_precision','model2_recall','model2_f1'))
plt.show()