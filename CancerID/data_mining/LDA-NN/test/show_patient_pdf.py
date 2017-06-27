'''
show the disease probability distribution over the test patients 
'''
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json

patient = 0
#disease dictionary
with open('../data/dis_dic.json') as json_file:
    data = json.load(json_file)
#diagnose probability result
diagnose_result = np.load('../result/simple_result.npy')
real_disease_matrix = pd.read_csv('../data/p_dis.csv')
test_patient = real_disease_matrix.iloc[patient+4847,:]
test_patient_real_disease_code = [int(item) for item in (test_patient[test_patient == 1].index)]

xs = np.arange(diagnose_result.shape[-1])
sorted_index = np.argsort(diagnose_result[patient,:])[::-1]
y = diagnose_result[patient,sorted_index]

key_list=[]
value_list=[]
for key,value in data.items( ):
    key_list.append(key)
    value_list.append(value)

sorted_icd_list_of_test_patient_disease = [key_list[value_list.index(i)] for i in sorted_index]
test_patient_real_disease_icd = [key_list[value_list.index(i)] for i in test_patient_real_disease_code]
# print 'xs'
# print xs
# print 'y'
# print y
# print 'new_x'
# print new_x
# print 'real_y'
# print real_y

sorted_real_disease_index_of_test_patient =  [sorted_icd_list_of_test_patient_disease.index(ys) for ys in test_patient_real_disease_icd  ]
# pick out > 0.8
index=0
for i in range(len(y)):
    index += y[i]
    if index > 0.8:
        index = i
        break

y = y[:index]          #probability 0.04 0.03 0.02 0.01 ...
xs = xs[:index]        # 0 1 2 3 4 ...

#real case in  0.8
filed_sorted_real_disease_index_of_test_patient = [filed for filed in sorted_real_disease_index_of_test_patient if filed < index ]

#pdf  in 0.8
sorted_icd_list_of_test_patient_disease = sorted_icd_list_of_test_patient_disease[:index]  # dis[0] dis[1] ...


plt.xlabel("Disease(ICD9)")
plt.ylabel("Probability")
# pdf of all disease (blue)
p1 = plt.bar(xs*2, y,width=1.5)
# red for real disease
y2 = np.zeros(len(xs))
y2[filed_sorted_real_disease_index_of_test_patient] = y[filed_sorted_real_disease_index_of_test_patient]
p2 = plt.bar(xs*2, y2,width=1.5,color='r')

plt.xticks(xs*2, sorted_icd_list_of_test_patient_disease, rotation=90 )
plt.legend((p1[0], p2[0]), ('prediction', 'real'))
plt.grid(linestyle = "-.")
plt.show()
