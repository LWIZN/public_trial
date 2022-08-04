from sndhdr import whathdr
import os
from flask import Flask, request
from mainProgram.identify import Manager

app = Flask(__name__)


@app.route('/')
def get_index():
    html = ''
    with open(f'./public/index.html', 'r', encoding='utf-8') as fin:
        for lien in fin.readlines():
            html = f'{html}{lien}'
    return html


@app.route('/src/<string:js_name>', methods=['GET'])
def get_js(js_name):
    with open(f'./src/{js_name}', 'r', encoding='utf-8') as fin:
        js_content = ''.join(fin.readlines())
    return js_content


@app.route('/start')
def start_pacakge():
    global wash_Machine
    print(f'was be trigged')
    os.system("node ./src/mainProgram/overMistake.js")
    try:
        message = Manager.get_user_voice_message()
        if Manager.in_black_list(message):
            return 'You was blocking'

        if (message == "一號"):
            account = '1號'
        else:
            account = '2號'

        Manager.start(account)

        return 'OK?'

    except Exception as e:
        print(e)
        return 'E~O~E~O'


@app.route('/take_cloths')
def take_cloths():
    Manager.is_taken = True
    return f'OK'


@app.route('/is_stop', methods=['POST'])
def stop():
    if request.method == 'POST':
        is_stop = request.values.get('stop')
        wash_Machine.is_taken = int(is_stop)
        return 'OK'
    else:
        return "GG"


if __name__ == '__main__':

    app.run()
