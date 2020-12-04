#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
【ドローン制御】

ドローンを自動離陸して、左→前→右→後へ移動する
簡単なドローン制御を行います。

1. UDPソケットの生成
2. コマンドモードにする
3. 自動離陸する
4. 左→前→右→後へ移動する
5. 自動着陸する
6. ソケットの解放

'''

import socket              # UDP通信
from time import sleep     # sleep用

# UDPソケットの生成
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tello_address = ('192.168.10.1', 8889)
print(socket)

# コマンドモードにする
cmd = 'command'
socket.sendto(cmd.encode('utf-8'), tello_address)
print(cmd)

# 自動離陸
cmd = 'takeoff'
socket.sendto(cmd.encode('utf-8'), tello_address)
print(cmd)
sleep(1)

# 左へ移動
cmd = 'left 60'
socket.sendto(cmd.encode('utf-8'), tello_address)
print(cmd)
sleep(5)

# 前方へ移動
cmd = 'forward 60'
socket.sendto(cmd.encode('utf-8'), tello_address)
print(cmd)
sleep(5)

# 右へ移動
cmd = 'right 60'
socket.sendto(cmd.encode('utf-8'), tello_address)
print(cmd)
sleep(5)

# 後方へ移動
cmd = 'back 60'
socket.sendto(cmd.encode('utf-8'), tello_address)
print(cmd)
sleep(5)

# 自動着陸
cmd = 'land'
socket.sendto(cmd.encode('utf-8'), tello_address)
print(cmd)

# ソケットを閉じる
socket.close()

