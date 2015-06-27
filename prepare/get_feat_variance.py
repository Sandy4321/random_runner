
p_learn = ('../raw_data/log_learn2.csv', '../data/variance_learn', '../raw_data/enrollment_learn.csv')
p_valid = ('../raw_data/log_valid2.csv', '../data/variance_valid', '../raw_data/enrollment_valid.csv')
p_train = ('../raw_data/log_train2.csv', '../data/variance_train', '../raw_data/enrollment_train.csv')
p_test = ('../raw_data/log_test2.csv', '../data/variance_test', '../raw_data/enrollment_test.csv')

import time
def get_day(date):
    arr = date.split('T')[0].split('-')
    if len(arr) != 3: return 0
    t = time.mktime([int(arr[0]), int(arr[1]), int(arr[2])] + [0]*6)
    return int(t)/3600/24

import json
import math 
for pin, pout, peid in [p_learn, p_valid, p_train, p_test]:
  key_num = {}
  for line in open(pin):
    arr = line.strip().split(',')
    #1,9Uee7oEuuMmgPx2IzPfFkWgkHZyPbWr0,DPnLzkJJqOOPRJfBxIHbQEERiYHu5ila,2014-06-14T09:38:29,server,nagivate,Oj6eQgzrdqBMlaCtaq1IkY6zruSrb71b
    #3,1qXC7Fjbwp66GPQc6pHLfEuO8WKozxG4,7GRhBDsirIGkRZBtSMEzNTyDr2JQm4xx,2014-06-19T08:43:59,server,access,jU152iC3MSAYCcXrcBy5IohAGjqKttZn,sequential,2014-06-19T00:00:00
    eid = arr[0]
    if eid not in key_num: key_num[eid] = {}
    day1 = get_day(arr[3])
    key_num[eid][day1] = key_num[eid].get(day1, 0) + 1
  key_num2 = {}
  for eid in key_num:
    key_num2[eid] = {}
    sort_list = sorted(key_num[eid].items(), key=lambda d:d[0])
    if len(sort_list) < 2: continue
    avg = sum([v2 for v1, v2 in sort_list]) / float(len(sort_list))
    std = math.sqrt(sum([(v2-avg)**2 for v1, v2 in sort_list]) / float(len(sort_list)))
    last_num = sort_list[-1][1]
    rate1 = last_num/avg
    rate2 = (last_num-avg)/std if std>0 else 0
    key_num2[eid]['lognum_avg'] = avg
    key_num2[eid]['lognum_std'] = std 
    key_num2[eid]['lognum_last'] = last_num 
    key_num2[eid]['lognum_last2avg'] = rate1 
    key_num2[eid]['lognum_last2std'] = rate2
  key_num = key_num2
  with open(pout, 'w') as fo:
    for line in open(peid):
        eid = line.split(',')[0]
        if eid in key_num:
            fo.write('%s\t%s\n' % (eid, json.dumps(key_num[eid])))

