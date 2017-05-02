#coding:utf-8

def key(line):
    if line.find('"V') > 0: return False
    elif line.find('Lymphangiole') > 0: return False
    elif line.find('alignant neoplasm') > 0: return True
    elif line.find('carcinoma') > 0: return True
    elif line.find('Kaposi\'s sarcoma') > 0: return True
    elif line.find('Hodgkin\'s') > 0: return True
    elif line.find('eticulosarcoma') > 0: return True
    elif line.find('Lymphosarcoma') > 0: return True
    elif line.find('lymphoma') > 0: return True
    elif line.find('Mycosis fungoides') > 0: return True
    elif line.find('Sezary\'s disease') > 0: return True
    elif line.find('Malignant histiocytosis') > 0: return True
    elif line.find('eukemic') > 0: return True
    elif line.find('Letterer-siwe disease') > 0: return True
    elif line.find('cell tumors') > 0: return True
    elif line.find('myeloma') > 0: return True
    elif line.find('immunoproliferative neoplasms') > 0: return True
    elif line.find('Myeloid sarcoma') > 0: return True
    elif line.find('Chronic erythremia') > 0: return True
    elif line.find('Malignant carcinoid') > 0: return True
    elif line.find('enign neoplasm') > 0: return True
    elif line.find('Lipoma') > 0: return True
    elif line.find('eiomyoma') > 0: return True
    elif line.find('Hemangioma') > 0: return True
    elif line.find('Lymphangioma') > 0: return True
    elif line.find('Neoplasm of un') > 0: return True
    elif line.find('eurofibromatosis') > 0: return True
    elif line.find('Schwannomatosis') > 0: return True
    elif line.find('Polycythemia vera') > 0: return True
    elif line.find('yelodysplastic syndrome') > 0: return True
    elif line.find('Essential thrombocythemia ') > 0: return True
    elif line.find('PTLD') > 0: return True
    elif line.find('lymphatic and') > 0: return True
    elif line.find('Neoplasms of un') > 0: return True
    else: return False

def cut(Line):
    icd = []
    for line in Line:
        i = 0
        cout = 2
        while cout > 0:
            if line[i] == '"':
                cout -= 1
                if cout == 1: start = i + 1
                elif cout == 0: end = i
            i += 1
        icd.append(line[start:end])
    return icd

with open("/home/zn/Documents/mimic/D_ICD_DIAGNOSES_DATA_TABLE.csv") as fin:
    #f2 = open("/home/zh/Desktop/MIMIC III/DIAGNOSES_ICD_DATA_TABLE.csv")
    lines = fin.readlines()
    
    Line = []
    for line in lines:
        if key(line):
            Line.append(line)
    #print Line
    with open('/home/zn/Desktop/cancer_icd9.txt', 'wb') as fout:
        for num in cut(Line):
            fout.write(num + '\n')

    '''lines = f2.readlines()
    n = 0
    for line in lines:
        print line[-2]'''


