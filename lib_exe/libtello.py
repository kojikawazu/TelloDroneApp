# -*- coding: utf-8 -*-
#!/usr/bin/env python

'''

Telloを使用する時に
呼びやすくしたライブラリ

'''

import socket               # UDP通信
from time import sleep      # sleep用
import threading            # スレッド
from msvcrt import getch    # キーボード関係
from cv2 import cv2         # openCV

# telloを使いやすくしたライブラリ
class libtello:
    
    def __init__(self):
        # TODO コンストラクタ
        print('生成')

        # キー番号辞書
        self.KEY = {
            'ESCAPE'      : 27,
            'KEY_P'       : 112,
            'KEY_Z'       : 122,
            'KEY_X'       : 120,
            'KEY_C'       : 99,
            'KEY_B'       : 98,
            'KEY_Q'       : 113,
            'KEY_W'       : 119,
            'KEY_E'       : 101,
            'KEY_R'       : 114,
            'KEY_SPEC'    : 224,
            'KEY_UP'      : 72,
            'KEY_DOWN'    : 80,
            'KEY_LEFT'    : 75,
            'KEY_RIGHT'   : 77,

            'KEY_UP_EX'   : 2490368,
            'KEY_DOWN_EX' : 2621440,
            'KEY_LEFT_EX' : 2424832,
            'KEY_RIGHT_EX': 2555904,
        }

        # 細かな設定
        self.response         = None
        self.isEnd            = False
        self.prevCnt          = 0
        self.isCameraEnd      = False
        self.cameraFrame      = None
        self.cameraReady      = False
        self.cameraThread     = None
        self.tello_movie_addr = 'udp://127.0.0.1:11111'
        self.tello_address    = ('192.168.10.1', 8889)
        self.localaddr        = ('0.0.0.0', 8890)

        # 送信用ソケット
        # 192.168.10.1のIPアドレスの8889ポート番号を設定
        # ドローンのIPアドレス
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        

        # 受信用ソケット
        # 受信IPアドレスと8890ポート番号を設定
        # ソケットをバインドし、ドローンからの受信を受け取る準備をする
        self.recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.recv_socket.bind(self.localaddr)

        # 受信スレッド開始
        # デーモン設定にするとこのプロセスが終了すると同時に
        # 受信スレッドも終了するようになる。
        self.recvThread = threading.Thread(target=self.recvSocket)
        self.recvThread.setDaemon(True)
        self.recvThread.start()
    # end init
    
    # 受信メソッド
    def recvSocket(self):
        # TODO 受信

        # isEndがFalseの間はループ
        while self.isEnd is False:
            try:
                # データを受け取る
                self.response, ip = self.recv_socket.recvfrom(1024)
            except socket.error as exc:
                print('error: %s' % exc)
        self.recv_socket.close()    # 受信ソケットの解放

    def getKeyValue(self, word):
        # TODO キー番号取得
        return self.KEY[word]
    
    def exec(self, word):
        # TODO ソケット送信
        print('[debug]: ' + word)
        self.socket.sendto(word.encode('utf-8'), self.tello_address)

    def exec_timer(self, word):
        # TODO ソケット送信(受信タイマー付き)
        self.abort_flg = False
        self.command_timeout = 0.8  # 800ミリ秒

        # タイマースレッド生成
        timer = threading.Timer(self.command_timeout, self.abort_flg)

        # ドローンへ指示送信
        print('[debug_timer]: ' + word)
        self.socket.sendto(word.encode('utf-8'), self.tello_address)

        # タイマー開始
        timer.start()
        while self.response is None:
            if self.abort_flg is True:
                break
        # タイマーキャンセル
        timer.cancel()

        # 受信後の処理
        if self.response is None:
            res = 'none_response'
        else:   # 返信ありの場合は文字列を受け取る
            res = self.response.decode('utf-8')
        self.response = None
        # 受信データを返す
        return res

    #　指示系
    def leftMove(self, speed):          # 左移動(20～500)
        self.exec('left ' + speed)
        self.setDoubleOperation()
    def rightMove(self, speed):         # 右移動(20～500)
        self.exec('right ' + speed)
        self.setDoubleOperation()
    def forwordMove(self, speed):       # 前方移動(20～500)
        self.exec('forward ' + speed)
        self.setDoubleOperation()
    def backMove(self, speed):          # 後方移動(20～500)
        self.exec('back ' + speed)
        self.setDoubleOperation()
    def upMove(self, speed):            # 上昇移動(20～500)
        self.exec('up ' + speed)
        self.setDoubleOperation()
    def downMove(self, speed):          # 下降移動(20～500)
        self.exec('down ' + speed)
        self.setDoubleOperation()
    def cwMove(self, speed):            # 時計回転(1～360)
        self.exec('cw ' + speed)
        self.setDoubleOperation()
    def ccwMove(self, speed):           # 半時計回転(1～360)
        self.exec('ccw ' + speed)
        self.setDoubleOperation()
    def flipMove(self, speed):          # 回転(l,r,f,b)
        self.exec('flip ' + speed)
        self.setDoubleOperation()

    def checkDoubleOperation(self):     # 二重操作防止チェック
        if self.prevCnt <= 0:
            return True
        else:
            return False

    def setDoubleOperation(self):       # 二重操作防止開始
        self.prevCnt = 1

    def prevDoubleOperation(self):      # 二重操作防止
        self.prevCnt += 1
        if self.prevCnt >= 2:
            self.prevCnt = 0

    # Camera
    def setCamera(self):
        # TODO カメラキャプチャー設定
        # tello_movie_addr = 'udp://0.0.0.0:11111'
        # IPアドレス 0.0.0.0
        # ポート番号 11111
        # ※ファイアーウォールの設定で11111ポートの受信許可の設定必要
        self.cap = cv2.VideoCapture(self.tello_movie_addr)
        if not self.cap.isOpened():
            self.cap.open(self.tello_movie_addr)
        if not self.cap.isOpened():
            self.cameraReady = False
        else:
            self.cameraReady = True

    def readCameraData(self):
        # TODO 1フレームずつ取得する
        if self.cameraReady is True:
            self.ret, self.cameraFrame = self.cap.read()
            if self.ret is False or self.cameraFrame is None:
                return False
            else:
                return True
        else:
            return False

    def showCamera(self):
        # TODO カメラ１フレーム表示
        if self.cameraReady is True:
           cv2.imshow("frame", self.cameraFrame)
    
    def releaseCamera(self):
        # TODO カメラ解放
        if self.cameraReady is True:
            self.cap.release()
            cv2.destroyAllWindows()

    def startCameraThread(self):
        # TODO カメラスレッドスタート
        self.cameraThread = threading.Thread(target=self.targetCameraThread)
        self.cameraThread.setDaemon(True)
        self.cameraThread.start()

    def endCameraThread(self):
        # TODO カメラスレッド終了フラグ立てる
        self.isCameraEnd = True

    def targetCameraThread(self):
        # TODO カメラスレッドの中身
        self.setCamera()                           # カメラの設定
        while self.isCameraEnd is False:
            for idx in range(10):
                ret = self.readCameraData()        # カメラデータ読込
            if ret is True:
                self.showCamera()                  # カメラフレーム表示
                cv2.waitKey(1)
        self.releaseCamera()                       # カメラの解放 

    # Mission Pad
    def goPad(self, dx, dy, dz, dspeed, dpadNum):
        # TODO
        # (dpadNum)パネルに(x:(dx),y:(dy),z:(dz))の座標へ
        # (dspeed)cm/sの速さで移動する
        self.exec('go ' + str(dx) + ' ' + str(dy) + ' ' + str(dz) + ' ' + str(dspeed) + ' ' + dpadNum)

    def jumpPad(self, dx, dy, dz, dspeed, dangle, dpadNumS, dpadNumE):
        # TODO
        # (dpadNumS)パネルに(x:(dx),y:(dy),z:(dz))の座標に(dspeed)cm/sの速さで移動する
        # その後、(dpadNumE)パネルに(x:(dx),y:(dy),z:(dz))の座標に(dspeed)cm/sの速さで移動した後
        # (dangle)°回転する
        self.exec('jump ' + dx + ' ' + dy + ' ' + dz + ' ' + dspeed + ' ' + 
                    dangle + ' ' + dpadNumS + ' ' + dpadNumE)

    def curvePad(self, dx1, dy1, dz1, dx2, dy2, dz2, dspeed, dpadNum):
        # TODO
        # (dpadNum)パネルに(x:(dx1),y:(dy1),z:(dz1))に(dspeed)cm/sの速さで移動し、
        # その後(x:(dx2),y:(dy2),z:(dz2))に(dspeed)cm/sの速さで移動する
        self.exec('curve ' + dx1 + ' ' + dy1 + ' ' + dz1 + ' ' +
                        dx2 + ' ' + dy2 + ' ' + dz2 + ' ' + dspeed + ' ' + dpadNum)

    # 取得系
    def get_battery(self):
        # TODO バッテリー残量取得
        battery = self.exec_timer('battery?')
        print('battery is ' + battery)

    # モード系
    def commandMode(self):              # コマンドモード
        self.exec('command')
    def monMode(self):                  # MissonPad オン
        self.exec('mon')    
    def mofMode(self):                  # MissonPad オフ
        self.exec('moff') 
    def streamonMode(self):             # カメラオンモード
        self.exec('streamon')
    def streamofMode(self):             # カメラオフモード
        self.exec('streamoff')
    def mdirection(self, mode):         # 前進、後退検出の設定
        # TODO
        # 0: 後退の検出のみ有効
        # 1: 前進の検出のみ有効
        # 2: 0と1のどちらも有効
        self.exec('mdirection ' + str(mode))
    
    def start(self):                    # 自動離陸
        self.exec('takeoff')
    def end(self):                      # 自動着陸
        self.isEnd = True               # スレッドの終了通知
        self.exec('land')               # 自動着陸
        self.socket.close()             # ソケットの解放

    # キー系
    def getKey(self):                   # キー取得
        return ord(getch())
    
    

