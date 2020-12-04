#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
【ドローン制御】

ミッションパッドを使用したドローン制御を行う。

1. UDP送信ソケットの生成
2. 受信用スレッドの開始
3. コマンドモードにする
4. ミッションパッド検出をオンにする
5. 自動離陸する
6. m1パッドに(0,0,100)の座標に60cm/sで移動する
7. m2パッドに(0,0,100)の座標に60cm/sで移動する
8. m1パッドに(0,0,100)の座標に60cm/sで移動する
9. ミッションパッド検出をオフにする
10. 自動着陸する
11. ソケットを閉じる
12. 受信用スレッドを終了させる

受信用スレッドの処理
1. UDP受信ソケットの生成
2. UDP受信ソケットのバインド
3. スレッド終了までループ
4. UDP受信ソケットの受信
5. 受信データを出力
6. 3へ戻る
7. UDP受信ソケットの解放

'''

import socket              # UDP通信
from time import sleep     # sleep用
import threading            # スレッド

def recvSocket():
    # TODO 受信メソッド

    # UDP受信用ソケット
    # IPアドレス(0.0.0.0)
    # ポート番号(8890) 
    recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    localaddr = ('0.0.0.0', 8890)
    # バインド
    recv_socket.bind(localaddr)
    print(recv_socket)

    while isEnd is False:
        try:
            # 受信処理
            response, ip = recv_socket.recvfrom(1024)
            # コマンドプロンプトに表示
            print(response.encode('utf-8'))
        except socket.error as exc:
            print('error: %s' % exc)
    # end while
    # ソケットを解放
    recv_socket.close()
# end def

# UDP送信用ソケットの生成
# IPアドレス(192.168.10.1)
# ポート番号(8889)
send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tello_address = ('192.168.10.1', 8889)
print(send_socket)

# UDP受信用スレッドの実行
# デーモンをTrueにするとプログラム終了したら
# スレッドも終了してくれる。
isEnd = False
recvThread = threading.Thread(target=recvSocket)
recvThread.setDaemon(True)
recvThread.start()

# コマンドモードにする
cmd = 'command'
send_socket.sendto(cmd.encode('utf-8'), tello_address)
print(cmd)

# ミッションパッド検出をオンにする
cmd = 'mon'
send_socket.sendto(cmd.encode('utf-8'), tello_address)
print(cmd)

# 自動離陸
cmd = 'takeoff'
send_socket.sendto(cmd.encode('utf-8'), tello_address)
print(cmd)
sleep(2)

# m1パッドに(0,0,100)の座標に60cm/sで移動する
cmd = 'go 0 0 100 60 m1'
send_socket.sendto(cmd.encode('utf-8'), tello_address)
print(cmd)
sleep(5)

# m2パッドに(0,0,100)の座標に60cm/sで移動する
cmd = 'go 0 0 100 60 m2'
send_socket.sendto(cmd.encode('utf-8'), tello_address)
print(cmd)
sleep(5)

# m1パッドに(0,0,100)の座標に60cm/sで移動する
cmd = 'go 0 0 100 60 m1'
send_socket.sendto(cmd.encode('utf-8'), tello_address)
print(cmd)
sleep(5)

# ミッションパッド検出をオフにする
cmd = 'moff'
send_socket.sendto(cmd.encode('utf-8'), tello_address)
print(cmd)

# 自動着陸
cmd = 'land'
send_socket.sendto(cmd.encode('utf-8'), tello_address)
print(cmd)

# ソケットを閉じる
send_socket.close()

# 受信用スレッドを終了させる
isEnd = True
sleep(3)



