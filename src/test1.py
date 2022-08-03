import json


with open('./src/black_list_tmp.json', 'r') as fin:
    jobj = json.load(fin)


print('one' in jobj[0])
