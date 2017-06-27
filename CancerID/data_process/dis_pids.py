# coding:utf-8

import json


def main():
    '''main()'''
    with open('/home/zn/Desktop/data/matrix/pid_less.txt', 'rb') as f:
        pid_ls = [p_id.strip() for p_id in f.readlines()]

    with open('/home/zn/Desktop/data/matrix/dis_dic.json', 'rb') as f:
        dis_id = json.load(f)
    dis_dic = {}
    for dis in dis_id:
        dis_dic[dis_id[dis]] = dis

    did_pid = {}
    with open('/home/zn/Desktop/data/matrix/p_dis.csv', 'rb') as f:
        count = 0
        for line in f.readlines():
            line = line.strip()
            dis_ls = line.split(',')
            for did in range(len(dis_ls)):
                if dis_ls[did] == '1':
                    disid = dis_dic[did]
                    if disid in did_pid:
                        did_pid[disid].add(pid_ls[count])
                    else:
                        did_pid[disid] = set([pid_ls[count]])
            count += 1

    for did in did_pid:
        did_pid[did] = ' '.join(did_pid[did])

    with open('/home/zn/Desktop/data/matrix/dis_pids.json', 'wb') as f:
        json.dump(did_pid, f)

if __name__ == '__main__':
    main()
