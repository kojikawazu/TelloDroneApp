#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
【ドローン制御】

ドローンのカメラを取得して、
PCに表示する

1. UDPソケットの生成
2. コマンドモードにする
3. ストリーム配信をオンにする
4. 自動離陸する
5. ドローン画面キャプチャーの生成
6. 無限ループ
7. 1フレームずつ取得する
8. 取得に失敗した場合
   13へ行く
9. 画面に出力する
10. キー状態を取得する
11. ESCAPEが入力されたら
    13へ行く
12. ここまで来たら6へ戻る
13. 自動着陸
14. ストリーム配信オフにする
15. OpenCVの解放
16. ソケットの解放

'''

import socket               # UDP通信
from time import sleep      # sleep用
from cv2 import cv2         # openCV

# UDP送信用ソケットの生成
# IPアドレス(192.168.10.1)
# ポート番号(8889)
send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tello_address = ('192.168.10.1', 8889)
print(send_socket)

# コマンドモードにする
cmd = 'command'
send_socket.sendto(cmd.encode('utf-8'), tello_address)
print(cmd)

# カメラ検出オンにする
cmd = 'streamon'
send_socket.sendto(cmd.encode('utf-8'), tello_address)
print(cmd)

# 自動離陸
cmd = 'takeoff'
send_socket.sendto(cmd.encode('utf-8'), tello_address)
print(cmd)
sleep(2)

# ドローン画面キャプチャーの生成
# IPアドレス(0.0.0.0)
# ポート番号(11111)
tello_movie_addr = 'udp://0.0.0.0:11111'
cap = cv2.VideoCapture(tello_movie_addr)
if not cap.isOpened():
    cap.open(tello_movie_addr)

while True:
    # 1フレームずつ取得する
    ret, frame = cap.read()

    # フレームが取得できなかった場合は、画面を閉じる
    if not ret:
        break

    # ウィンドウに出力
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    # ESCキーを入力されたら画面を閉じる
    if key == 27:
        break
#end ehile

# 自動着陸
cmd = 'land'
send_socket.sendto(cmd.encode('utf-8'), tello_address)
print(cmd)

# カメラ検出オフにする
cmd = 'streamoff'
send_socket.sendto(cmd.encode('utf-8'), tello_address)
print(cmd)

# OpenCVの解放
cap.release()
cv2.destroyAllWindows()

# ソケットを閉じる
send_socket.close()