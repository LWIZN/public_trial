import speech_recognition as sr
import time
import threading
import re
import requests
import cv2
import argparse
import os

is_taken = 0

mistake_counter = 0

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

DELAY = 1.0
COUNTDOWN = 3

url = 'https://notify-api.line.me/api/notify'
token = 'D1FEkBMkPzH6TwzNgp4XDxC9xrDpIcZuCizjUi9T4GG'
headers = {
    'Authorization': 'Bearer ' + token    # 設定權杖
}
# data = {
#     'message':'測試一下！' ,    # 設定要發送的訊息
#     # 'imageThumbnail':'http://event.family.com.tw/2016_pokemon/images/blanket-deco-pikachu.png',
#     # 'imageFullsize':'http://event.family.com.tw/2016_pokemon/images/blanket-deco-pikachu.png'
#     # 'imageThumbnail': 'D:\DIGI\必修\Washer\public_trial\pic'
# }

# event_name_line='Send_Line'
# key='b48sBWmSpULW-H4pCynRgc'
# URL_line='https://maker.ifttt.com/trigger/' + event_name_line + '/with/key/' + key


session = requests.Session()


def take_picture(video, picture_path, id):
    # 選擇攝影機
    cap = cv2.VideoCapture(video)
    # 設定影像的尺寸大小
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

    PRE_SECOND = time.time()
    count = 0
    while(count <= COUNTDOWN):
        ret, frame_src = cap.read()

        cv2.putText(frame_src,
                    str(COUNTDOWN - count),
                    (int(CAMERA_WIDTH*0.9), int(CAMERA_HEIGHT*0.08)),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 255, 0), 6, cv2.LINE_AA)
        cv2.putText(frame_src,
                    str(COUNTDOWN - count),
                    (int(CAMERA_WIDTH*0.9), int(CAMERA_HEIGHT*0.08)),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 0, 0), 2, cv2.LINE_AA)

        cv2.imshow('Standing by ....', frame_src)

        POST_SECOND = time.time()
        if POST_SECOND - PRE_SECOND >= DELAY:
            count = count + 1
            PRE_SECOND = time.time()

        cv2.waitKey(1)

    ret, frame_src = cap.read()
    cv2.imshow('Picture', frame_src)
    cv2.waitKey(1)
    time.sleep(1)
    cv2.imwrite(picture_path + str(id)+'.jpg', frame_src)

    # 釋放攝影機
    cap.release()
    # 關閉所有 OpenCV 視窗
    cv2.destroyAllWindows()


try:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--path', help='File path of *.jpg file.', required=True)
    parser.add_argument(
        '--video', help='Camera number.', required=True, type=int)
    args = parser.parse_args()

    folder = os.path.exists(args.path)

    # 判斷結果
    if not folder:
        # 如果不存在，則建立新目錄
        os.makedirs(args.path)
        print('資料夾 ' + args.path + ' 建立成功')

    else:
        # 如果目錄已存在，則不建立，提示目錄已存在
        print('資料夾 ' + args.path + ' 已存在')

    while True:
        r = sr.Recognizer()
        m = sr.Microphone()
        m.RATE = 44100
        m.CHUNK = 512

        print("A moment of silence, please...")
        with m as source:
            r.adjust_for_ambient_noise(source)
            if (r.energy_threshold < 2000):
                r.energy_threshold = 2000
            print("Set minimum energy threshold to {}".format(r.energy_threshold))

            print("Say something!")
            audio = r.listen(source)
            print("Got it! Now to recognize it...")

            # Load Google Speech Recognition API
            speechtext = r.recognize_google(
                audio, language='zh', show_all=True)
            print(type(speechtext))  # dict

            if len(speechtext) == 0:
                pass
            else:
                speechtext = speechtext['alternative'][0]['transcript']
                speechtext = speechtext.replace(' ', '')
                print("You said: " + speechtext)

                # if re.search('\s*照相\s*',speechtext):
                #     take_picture(args.video, args.path)
                #     print('已拍照')

                # elif re.search('\s*結束程式\s*',speechtext):
                #     print('結束程式運作')
                #     break
                URL_line1 = 'https://maker.ifttt.com/trigger/Send_Line/with/key/b48sBWmSpULW-H4pCynRgc'
                URL_line2 = 'https://maker.ifttt.com/trigger/tina_Line/with/key/ctaeW71uoRjnvtZnNNpd8z'
                URL_sheets = 'https://maker.ifttt.com/trigger/send_sheets/with/key/mSWScH-gX3M1yBnXbcwgSuTQjrmG8vPV1kiwDDrgei7'

                if re.search('一號\s*', speechtext):

                    take_picture(args.video, args.path, 1)
                    print('1號已拍照')
                    current_time = time.time()
                    end_time = time.time() + 30
                    r_line = session.post(URL_line1, params={"value1": '學號: '+'1號', "value2": '開始時間:'+str(
                        time.ctime(current_time)), "value3": '結束時間: '+str(time.ctime(end_time))})
                    time.sleep(10)
                    r_line = session.post(URL_line1, params={
                                          "value1": '學號: '+'1號', "value2": '注意注意!剩下20秒鐘!', "value3": '結束時間: '+str(time.ctime(end_time))})
                    time.sleep(10)
                    r_line = session.post(URL_line1, params={
                                          "value1": '學號: '+'1號', "value2": '還有10秒,跑起來! 不要遲到了!!!', "value3": '結束時間: '+str(time.ctime(end_time))})
                    time.sleep(10)

                    r_line = session.post(URL_line2, params={
                                          "value1": '學號: '+'1號', "value2": '時間到!!!!', "value3": '不想被公審的話你還有三秒鐘'})
                    time.sleep(3)
                    if is_taken == 0:

                        mistake_counter += 1
                        if mistake_counter > 3:
                            os.system("node ./main.js")

                        r_line = session.post(URL_line2, params={
                                              "value1": '學號: '+'1號', "value2": '時間到!!!!', "value3": '準備被公審吧!'})
                        r_sheets = session.post(
                            URL_sheets, params={"value1": '1'})

                        # 傳到群組
                        data = {
                            'message': '學號: 1號, 洗衣服超時記點一次，公審他!!!',    # 設定要發送的訊息
                        }
                        file = {'imageFile': open(
                            'D:\DIGI\必修\Washer\public_trial\pic/1.jpg', 'rb')}
                        data = requests.post(
                            url, headers=headers, data=data, files=file)   # 使用 POST 方法
                    if is_taken == 1:
                        r_line = session.post(
                            URL_line2, params={"value1": '學號: '+'1號', "value2": '你好棒', "value3": '你是好寶寶'})

                if re.search('2號\s*', speechtext):
                    take_picture(args.video, args.path, 2)

                    current_time = time.time()
                    end_time = time.time() + 30
                    print('2號已拍照')
                    r_line = session.post(URL_line2, params={"value1": '學號: '+'2號', "value2": '開始時間:'+str(
                        time.ctime(current_time)), "value3": '結束時間: '+str(time.ctime(end_time))})
                    time.sleep(10)
                    r_line = session.post(URL_line2, params={
                                          "value1": '學號: '+'2號', "value2": '注意注意!剩下20秒鐘!', "value3": '結束時間: '+str(time.ctime(end_time))})
                    time.sleep(10)
                    r_line = session.post(URL_line2, params={
                                          "value1": '學號: '+'2號', "value2": '還有10秒,跑起來! 不要遲到了!!!', "value3": '結束時間: '+str(time.ctime(end_time))})
                    time.sleep(10)
                    r_line = session.post(URL_line2, params={
                                          "value1": '學號: '+'2號', "value2": '時間到!!!!', "value3": '不想被公審的話你還有三秒鐘'})
                    time.sleep(3)
                    if is_taken == 0:

                        mistake_counter += 1
                        if mistake_counter > 3:
                            os.system("node ./main.js")

                        r_line = session.post(URL_line2, params={
                                              "value1": '學號: '+'2號', "value2": '時間到!!!!', "value3": '準備被公審吧!'})
                        r_sheets = session.post(
                            URL_sheets, params={"value1": '2'})
                        # 傳到群組
                        data = {
                            'message': '學號: 2號, 洗衣服超時記點一次，公審他!!!',    # 設定要發送的訊息
                        }
                        file = {'imageFile': open(
                            'D:\DIGI\必修\Washer\public_trial\pic/2.jpg', 'rb')}
                        data = requests.post(
                            url, headers=headers, data=data, files=file)   # 使用 POST 方法
                    if is_taken == 1:
                        r_line = session.post(URL_line2, params={
                                              "value1": '學號: '+'2號', "value2": '時間到!!!!', "value3": '你好棒'})


except KeyboardInterrupt:
    print("Quit")
