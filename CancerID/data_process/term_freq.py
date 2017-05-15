#coding:utf-8

import pymongo
import json

def term_freq():
    pass

def main():
    conn = pymongo.MongoClient()
    mimic = conn.mimic
    diag_icd = mimic.DIAGNOSES_ICD
    icd_dic = {}
    icd_ls = []
    icd_id = 0
    with open('/home/zn/Desktop/icd_label.txt', 'wb') as f:
        p_icd = {}
        for line in diag_icd.find():
            icd9 = line['ICD9_CODE']
            if icd9 in icd_dic:
                p_icd[icd_dic[icd9]].add(line['SUBJECT_ID'])
            else:
                icd_dic[icd9] = icd_id
                p_icd[icd_dic[icd9]] = set([line['SUBJECT_ID']])
                icd_id += 1
        #print p_icd
                    
        for icd in p_icd:
            for p in p_icd[icd]:
                icd_ls.append({'icd_id':icd, 'SUBJECT_ID':p})
        print len(icd_ls)
        icd_ls.sort(key = lambda x: x['icd_id'])
        for icd in icd_ls:
            f.write(str(icd['icd_id']) + '\n')
    with open('/home/zn/Desktop/icd.json', 'wb') as f:
        json.dump(icd_dic, f)
    
    test = conn.test
    p_docs = test.patient_docs
    tf_all = {}
    term_id = 0
    n = 0
    with open('/home/zn/Desktop/tf_part.txt', 'wb') as f:
        for icd in icd_ls:
            line = p_docs.find_one({'SUBJECT_ID':icd['SUBJECT_ID']})
            tf_part = {}
            term_ls = line['document'].split('\t')
            for term in term_ls:
                if term:
                    if term in tf_all:
                        if term in tf_part:
                            tf_part[term][1] += 1
                        else:
                            tf_part[term] = [tf_all[term], 1]
                    else:
                        term_id += 1
                        tf_all[term] = term_id
                        tf_part[term] = [term_id, 1]
            tf_ls = []
            for k in tf_part:
                tf_ls.append({'id':tf_part[k][0], 'tf':tf_part[k][1], 'word':k})
            tf_ls.sort()
            f.write(str(len(tf_ls)))
            for i in tf_ls:
                f.write(' '+str(i['id'])+':'+str(i['tf']))
            f.write('\n')
            n += 1
            print n

    
    with open('/home/zn/Desktop/tf_all.json', 'wb') as f:
        json.dump(tf_all, f)

if __name__ == '__main__':
    main()