

def reader(path, num):
    with open('/home/zn/Documents/PRESCRIPTIONS.csv', 'wb') as fout:
        with open(path, 'rb') as f:
            for i in range(num):
                fout.write(f.readline())

path = '/home/zn/Documents/MIMIC/PRESCRIPTIONS_DATA_TABLE.csv'
reader(path, 100000)