import json
import os


with open('./src/black_list_tmp.json', 'r') as fin:
    jobj = json.load(fin)


print('two' in jobj)


os.system("node ./src/mainProgram/overMistake.js")
