#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
【ドローン制御】

ミッションパッドを使用したドローン制御を行う。

1. libtelloの生成
2. コマンドモードにする
3. ミッションパッド検出をオンにする
4. 前方、後方の検出をオンにする
5. 自動離陸する
6. m1パネルに(x:0,y:0,z:100)の座標へ10cm/sの速さで移動する
7. m2パネルに(x:0,y:0,z:100)の座標へ10cm/sの速さで移動する
8. m3パネルに(x:0,y:0,z:100)の座標へ10cm/sの速さで移動する
9. ミッションパッド検出をオフにする
10. 自動着陸する
    ※ endメソッドでソケットの解放等行ってます。

'''

from time import sleep          # sleep用
from libtello import libtello   # 自作ライブラリ


if __name__ == "__main__":
    # TODO メイン
    test = libtello()

    # コマンドモードチェンジ
    test.commandMode()

    # Mission Padオン
    test.monMode()

    # mdirection設定
    test.mdirection(2)

    # 離陸
    test.start()

    sleep(5)

    # m1パネルに(x:0,y:0,z:100)の座標へ10cm/sの速さで移動する
    test.goPad(0, 0, 140, 60, 'm1')
    sleep(3)

    test.goPad(0, 0, 140, 60, 'm2')
    sleep(3)

    test.goPad(0, 0, 140, 60, 'm3')
    sleep(3)

    test.goPad(0, 0, 140, 60, 'm2')
    sleep(3)

    test.goPad(0, 0, 140, 60, 'm1')
    sleep(3)

    # Mission Padの検出を無効にする
    test.mofMode()

    # 自動着陸モードに入る
    # ソケットを閉じて終了に入る
    test.end()

    # main end

    







    

