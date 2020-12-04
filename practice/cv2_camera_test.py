#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
【ドローン制御】

パソコンのカメラをキャプチャーするアプリ

1. 画面キャプチャーの設定をする
2. キャプチャーオブジェクトが開かれてない場合
   もう一度開く
3. 無限ループ
4. 1フレームずつ取得する
5. フレームが取得できなかった場合は、
   9へ行く
6. ウィンドウに出力
7. ESCキーを入力されたら
　 9へ行く
8. ここまで来たら3へ戻る
9. 受信用スレッドの終了

'''

from time import sleep      # sleep用
from cv2 import cv2         # openCV

# 画面キャプチャーの生成
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    cap.open(0)

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

# OpenCVの解放
cap.release()
cv2.destroyAllWindows()






