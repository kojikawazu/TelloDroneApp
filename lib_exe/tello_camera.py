#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
【ドローン制御】

ドローンのカメラを取得して、
PCに表示する

1. libtelloの生成
2. コマンドモードにする
3. ストリーム配信をオンにする
4. 自動離陸する
5. カメラの設定
6. 無限ループ
7. 1フレームずつ取得する
8. 取得に失敗した場合
   14へ行く
9. カウントする
10. もし10で割って余りが0の場合,
    時計回りに45°回転する
11. ウィンドウに出力ESCAPEが入力されたら
12. ESCAPEが入力されたら
    14へ行く
13. ここまで来たら6へ戻る
14. カメラの解放
15. ストリーム配信をオフにする
16. 自動着陸
    ※ endメソッドでソケットの解放等行ってます。

'''

from time import sleep         # sleep用
from cv2 import cv2            # openCV
from libtello import libtello  # 自作ライブラリ

if __name__ == "__main__":
    print('開始')
    test = libtello()

    # コマンドモード
    test.commandMode()

    # カメラオン
    test.streamonMode()

    # 離陸
    test.start()

    sleep(3)
    # カメラの設定
    test.setCamera()

    cnt = 0
    while True:
        # 1フレームずつ取得する
        ret = test.readCameraData()
        
        # フレームが取得できなかった場合は、画面を閉じる
        if ret is False:
            break

        cnt += 1
        if cnt % 10 == 0:
            test.cwMove('45')

        # ウィンドウに出力
        test.showCamera()
        key = cv2.waitKey(1)
        # ESCキーを入力されたら画面を閉じる
        if key == test.getKeyValue('ESCAPE'):
            break

    # end while

    # カメラの解放
    test.releaseCamera()

    # カメラオフ
    test.streamofMode()

    # 着陸
    test.end()
    print('終了')










