# coding:utf-8

'''生成每个疾病下的应检查项目，检查项目是所有患此病的病人的检查项目之间的交集'''

import json

import pymongo


def main():
    '''main()'''
    with open('/home/zn/Desktop/data/matrix/dis_pids.json', 'rb') as f_r:
        dis_pids = json.load(f_r)
    for dis in dis_pids:
        dis_pids[dis] = dis_pids[dis].split()

    # mimic = pymongo.MongoClient().mimic
    # chart = mimic.CHARTEVENTS
    # lab = mimic.LABEVENTS
    # out = mimic.OUTPUTEVENTS
    # micro = mimic.MICROBIOLOGYEVENTS
    with open('/home/zn/Desktop/data/matrix/dis_dic.json', 'rb') as f:
        dis_dic = json.load(f)

    dis_exc = ["1983", "1628", "20280", "1977", "1985", "2113", "1970"]

    dis_kno = pymongo.MongoClient('118.89.186.110').knowledge.disease_knowledge
    # dis_item.remove()

    for item in dis_dic:
        if item not in dis_exc:
            dis_kno.insert_one({'ICD9_CODE':item, 'ITEMS':''})
        else:
            print '\n', item

    #3, 4, 6, 10, 43, 35, 30
    #"1983", "1628", "20280", "1977", "1985", "2113", "1970"
    #36, 80, 145, 200, 266, 300, 385, 446, 591, 788, 883, 1112

    '''did_ls = ["1977", "1985", "2113", "1970"]
    for did in did_ls:
        item_set = set()
        for pid in dis_pids[did]:
            item_ls = []
            item = set()
            for doc in chart.find({'SUBJECT_ID':pid}):
                item.add(doc['ITEMID'])
            for doc in out.find({'SUBJECT_ID':pid}):
                item.add(doc['ITEMID'])
            for doc in micro.find({'SUBJECT_ID':pid}):
                item.add(doc['SPEC_ITEMID'])
            for doc in lab.find({'SUBJECT_ID':pid}):
                item.add(doc['ITEMID'])
            item_ls.append(item)
            print len(item_ls),
        # for i in range(len(item_ls)):
        for i, item in enumerate(item_ls):
            if i == 0:
                item_set = item_ls[i]
            else:
                item_set = item_set & item_ls[i]

        print len(item_set)
        items = ' '.join(item_set)
        dis_item.insert_one({'ICD9_CODE':did, 'ITEMS':items})
        print did'''

if __name__ == '__main__':
    main()
