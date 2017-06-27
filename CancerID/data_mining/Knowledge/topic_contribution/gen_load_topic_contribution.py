import pickle
from datetime import datetime
import pprint
from pymongo import MongoClient
import json
client = MongoClient()
fil = open('../data/new_support_dict.pkl','rb')
with open('../data/dis_dic.json','rb') as f:
    dic = json.load(f)

topic = pickle.load(fil)
pprint.pprint(topic)
print(dic)
for number in range(416): 
    for key, value in dic.items():
        if value == number:
            print(number)
            try: 
                client.knowledge.topic_contribution.insert_one({'key':str(key),'contrib':topic[number],'time':datetime.now()})
            except:
                client.knowledge.topic_contribution.insert_one({'key':str(key),'contrib':{'11': '0', '10': '0','13': '0', '12': '0', '15': '0', '14': '0', '17': '0', '16': '0', '19': '0', '18': '0', '1': '0', '0': '0', '3': '0', '2': '0', '5': '0', '4': '0', '7': '0', '6': '0', '9': '0', '8': '0'},'time':datetime.now()})
