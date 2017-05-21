import csv
import time
import json

def search(subj_id):
    data = {}

    files = ['/home/zn/Documents/mimic/DIAGNOSES_ICD_DATA_TABLE.csv',
             '/home/zn/Documents/mimic/DRGCODES_DATA_TABLE.csv',
             '/home/zn/Documents/mimic/LABEVENTS_DATA_TABLE.csv',
             '/home/zn/Documents/mimic/PATIENTS_DATA_TABLE.csv',
             '/home/zn/Documents/mimic/NOTEEVENTS_DATA_TABLE.csv',
             '/media/zn/00051A0B00093CEE/mimic/CHARTEVENTS_DATA_TABLE.csv',
             '/home/zn/Documents/MIMIC/ADMISSIONS_DATA_TABLE.csv',
             '/home/zn/Documents/MIMIC/CALLOUT_DATA_TABLE.csv',
             '/home/zn/Documents/MIMIC/CPTEVENTS_DATA_TABLE.csv',
             '/home/zn/Documents/MIMIC/DATETIMEEVENTS_DATA_TABLE.csv',
             '/home/zn/Documents/MIMIC/ICUSTAYS_DATA_TABLE.csv',
             '/home/zn/Documents/MIMIC/INPUTEVENTS_CV_DATA_TABLE.csv',
             '/home/zn/Documents/MIMIC/INPUTEVENTS_MV_DATA_TABLE.csv',
             '/home/zn/Documents/MIMIC/MICROBIOLOGYEVENTS_DATA_TABLE.csv',
             '/home/zn/Documents/MIMIC/OUTPUTEVENTS_DATA_TABLE.csv',
             '/home/zn/Documents/MIMIC/PRESCRIPTIONS_DATA_TABLE.csv',
             '/home/zn/Documents/MIMIC/PROCEDUREEVENTS_MV_DATA_TABLE.csv',
             '/home/zn/Documents/MIMIC/PROCEDURES_ICD_DATA_TABLE.csv',
             '/home/zn/Documents/MIMIC/SERVICES_DATA_TABLE.csv',
             '/home/zn/Documents/MIMIC/TRANSFERS_DATA_TABLE.csv'
             ]
             #'/media/zn/00051A0B00093CEE/mimic/CHARTEVENTS_DATA_TABLE.csv'
             #'/home/zn/Documents/mimic/NOTEEVENTS_DATA_TABLE.csv'
    
    with open('/home/zn/Desktop/patient_info_2.txt', 'wb') as fout:
        for file in files: 
            with open(file, 'rb') as f:
                fout.write('#' + file + '\n\n')
                reader = csv.DictReader(f)
                f1 = 0
                f2 = 0
                for line in reader:
                    if line['SUBJECT_ID'] == subj_id:
                        #data.update(line)
                        json.dump(line,fout,ensure_ascii=False)
                        fout.write('\n')
                        f1 +=1
                        f2 = 0
                    else: f2 = -1
                    if f1 > 1 and f2 < 0:break
                
                fout.write('\n')
    #print data

'''def search1(subj_id):
    data = {}

    files = ['/home/zn/Documents/mimic/DIAGNOSES_ICD_DATA_TABLE.csv',
             '/home/zn/Documents/mimic/DRGCODES_DATA_TABLE.csv',
             '/home/zn/Documents/mimic/LABEVENTS_DATA_TABLE.csv',
             '/home/zn/Documents/mimic/PATIENTS_DATA_TABLE.csv',
             ]
             #'/media/zn/00051A0B00093CEE/mimic/CHARTEVENTS_DATA_TABLE.csv'
             #'/home/zn/Documents/mimic/NOTEEVENTS_DATA_TABLE.csv'
    
    for file in files: 
        with open(file, 'rb') as f:
            reader = csv.Reader(f)
            for line in reader:
                if line['SUBJECT_ID'] == subj_id:
                    data.update(line)
                    
    print data'''

s1 = time.clock()
search('2603')
e1 = time.clock()
print "\ncost time " + str(e1-s1)