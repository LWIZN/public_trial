import speech_recognition as sr
import time
import datetime as dt
import requests
import cv2
import os
import json

__all__ = ['Manager']

SHEETS_URL = 'https://maker.ifttt.com/trigger/send_sheets/with/key/mSWScH-gX3M1yBnXbcwgSuTQjrmG8vPV1kiwDDrgei7'
DELAY = 1.0
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
LINE_GROUP_URL = 'https://notify-api.line.me/api/notify'
LINE_GROUP_TOKEN = 'D1FEkBMkPzH6TwzNgp4XDxC9xrDpIcZuCizjUi9T4GG'


class WashMacnineManager:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.default_black_list_path = "./src/black_list_tmp.json"
        self.student_map = {
            # '1號': 'https://maker.ifttt.com/trigger/send_line/with/key/mSWScH-gX3M1yBnXbcwgSuTQjrmG8vPV1kiwDDrgei7',
            # '2號': 'https://maker.ifttt.com/trigger/send_line/with/key/mSWScH-gX3M1yBnXbcwgSuTQjrmG8vPV1kiwDDrgei7'

            '1號': 'https://maker.ifttt.com/trigger/Send_Line/with/key/b48sBWmSpULW-H4pCynRgc',
            '2號': 'https://maker.ifttt.com/trigger/tina_Line/with/key/ctaeW71uoRjnvtZnNNpd8z'
        }

    def _load_black_list(self, path) -> dict:
        with open(path, 'r') as fin:
            return json.load(fin)

    def in_black_list(self, message: str) -> bool:
        self.black_list = self._load_black_list(self.default_black_list_path)
        if (message == "一號"):
            message = "one"
        else:
            message = "two"
        return (message in self.black_list)

    def get_user_voice_message(self):
        self.microphone.RATE = 44100
        self.microphone.CHUNK = 512
        print("A moment of silence, please...")
        with self.microphone as source:
            while True:
                self.recognizer.adjust_for_ambient_noise(source)
                if self.recognizer.energy_threshold < 2000:
                    self.recognizer.energy_threshold = 2000
                    print(
                        f"Set minimum energy threshold to {self.recognizer.energy_threshold}")

                print("Say something!")
                audio = self.recognizer.listen(source)
                print("Got it! Now to recognize it...")
                speechtext = self.recognizer.recognize_google(
                    audio, language='zh', show_all=True)

                if len(speechtext) > 0:
                    speechtext = speechtext['alternative'][0]['transcript']
                    speechtext = speechtext.replace(' ', '')
                    print("You said: " + speechtext)
                    return speechtext

    def take_picture(self, video, picture_path, id):
        cap = cv2.VideoCapture(video, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
        ret, frame_src = cap.read()
        print(ret)
        cv2.imshow('picture', frame_src)
        cv2.imwrite(picture_path + str(id)+'.jpg', frame_src)
        cap.release()
        cv2.destroyAllWindows()

    def start(self, account):
        self.is_taken = False
        ID = ''
        if (account == '1號'):
            ID = '1'
        else:
            ID = '2'

        def ifttt_post(student_serial, value2, value3):
            tmp = requests.post(self.student_map[student_serial], params={
                'value1': f'學號: {student_serial}',
                'value2': value2,
                'value3': value3
            })
            tmp.close()

        def group_post(message, media_path):
            headers = {
                'Authorization': f'Bearer {LINE_GROUP_TOKEN}'
            }
            params = {
                'message': message,
                'imageFile': open(media_path)
            }
            tmp = requests.post(LINE_GROUP_URL, headers=headers, params=params)
            tmp.close()

        path = './DCIM'
        video = 0
        self.take_picture(video, path, ID)

        first_warning = False
        seconds_warning = False
        last_warning = False
        first_round = True

        folder = os.path.exists(path)

        if not folder:
            os.makedirs(path)
            print('資料夾 ' + path + ' 建立成功')

        else:
            print('資料夾 ' + path + ' 已存在')

        start_time = dt.datetime.now().replace(microsecond=0)
        end_time = start_time + dt.timedelta(0, 30)

        while True:
            duration = dt.datetime.now() - start_time
            if first_round:
                ifttt_post(
                    account, f'開始時間: {start_time.time()}', f'結束時間: {end_time.time()}')
                first_round = False
                print('Timing begins')

            if self.is_taken:
                print('is_taken')
                ifttt_post(account, '你好棒', '你是好寶寶')
                break

            if 9 < duration.seconds < 11 and not first_warning:
                print(f'a least 20 sec')
                ifttt_post(account, '注意注意!剩下20秒鐘!', f'結束時間: {end_time.time()}')
                first_warning = True
            elif 19 < duration.seconds < 21 and not seconds_warning:
                print(f'a least 10 sec')
                ifttt_post(account, '還有10秒,跑起來! 不要遲到了!!!',
                           f'結束時間: {end_time.time()}')
                seconds_warning = True

            elif 29 < duration.seconds < 31 and not last_warning:
                last_warning = True
                print('time out')
                ifttt_post(account, '時間到!!!!', '不想被公審還有三秒')
                time.sleep(3)

                if not self.is_taken:
                    ifttt_post(account, value2=f'時間到!!!!', value3='準備被公審吧!')
                    requests.post(SHEETS_URL, params={
                        "value1": ID})
                    group_post(message=f'學號: {account}',
                               media_path='./' + str(id)+'.jpg')
                else:
                    ifttt_post(account, '你好棒', '你是好寶寶')
                break

    def update_black_list(self, new_black_path=None):
        path = self.default_black_list_path if new_black_path is None else new_black_path

        with open(path, 'r') as fin:
            self.black_list = json.load(fin)

    def reset(self):
        self.is_taken = False
        self.update_black_list()


Manager = WashMacnineManager()
