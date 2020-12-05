# -*- coding: utf-8 -*-
#!/usr/bin/env python

'''

ドローンのカメラを取得して画面に表示し
キーボードでドローンを制御するアプリ

メインメソッドの以下の箇所を注目。
Nが0に指定した場合、カメラは使いません。
Nが1に指定した場合、カメラを使用します。
test = telloClass(N)

[メインメソッド]
1. telloClassを生成
2. telloClassを実行

[telloClass]

〇生成時
1. カメラフラグの設定
2. libtelloライブラリの生成

〇実行時
1. コマンドモードを送信
2. カメラモードをオンにする
3. 自動離陸する
4. カメラの設定を行う
5. 無限ループ
6. 二重操作防止処理
7. キー取得
8. キー判定
   ESCAPEキーが押されたら10へ行く
9. ここまで来たら5へ戻る
10. カメラモードをオフにする
11. カメラを解放
12. 自動離陸＆ソケットの解放＆スレッドの停止

'''

from time import sleep          # sleep用
from libtello import libtello   # 自作ライブラリ

# ドローンクラス(キー+カメラ)
class telloClass:
    def __init__(self, cameraFlg):
        # TODO 初期化
        # cameraFlg
        # 0ならカメラを使用しない
        # 1ならカメラを使用する

        self.cameraFlg = cameraFlg              # カメラフラグ設定
        self.test      = libtello()             # 自作ライブラリ生成

    def exe(self):    
        # TODO 実行   
        self.test.commandMode()                 # コマンド実行
        if self.cameraFlg is 1:                 
            self.test.streamonMode()            # カメラモードオン

        self.test.start()                       # 自動離陸        
        sleep(1)
        if self.cameraFlg is 1:                 # カメラ設定
            self.test.startCameraThread()
 
        print('開始')
        while True:
            sleep(1)                                         # 1秒スリープ
            if self.test.checkDoubleOperation() is False:    # 二重操作防止                         # 二重キー操作防止策
                self.test.prevDoubleOperation()
            else:
                # キー取得
                key = self.test.getKey() 
                print(key)
                # キー判定
                if key == self.test.getKeyValue('ESCAPE') : # エスケープ                  
                   break                                    # 終了
                elif key == self.test.getKeyValue('KEY_P') :# Pキー
                    self.test.get_battery()                 # バッテリー残量取得
                elif key == self.test.getKeyValue('KEY_Z') :# Zキー
                    self.test.upMove('40')                  # 上昇
                elif key == self.test.getKeyValue('KEY_X') :# ｘキー
                    self.test.downMove('40')                # 下降
                elif key == self.test.getKeyValue('KEY_C') :# cキー
                    self.test.cwMove('360')                 # 時計回りに回転
                elif key == self.test.getKeyValue('KEY_B') :# bキー
                    self.test.ccwMove('360')                # 反時計回りに回転
                elif key == self.test.getKeyValue('KEY_Q') :# Qキー
                    self.test.flipMove('l')                 # 左宙返り
                elif key == self.test.getKeyValue('KEY_W') :# Wキー
                    self.test.flipMove('r')                 # 左宙返り
                elif key == self.test.getKeyValue('KEY_E') :# Eキー
                    self.test.flipMove('f')                 # 左宙返り
                elif key == self.test.getKeyValue('KEY_R') :# Rキー
                    self.test.flipMove('b')                 # 左宙返り
                elif key == self.test.getKeyValue('KEY_SPEC') :    # スペシャルキー
                    key = self.test.getKey()                       # もう一度キー取得
                    if key == self.test.getKeyValue('KEY_UP'):        # 上
                        self.test.forwordMove('40')                   # 前方移動
                    elif key == self.test.getKeyValue('KEY_DOWN'):    # 下
                        self.test.backMove('40')                      # 後方移動
                    elif key == self.test.getKeyValue('KEY_LEFT'):    # 左
                        self.test.leftMove('40')                      # 左へ移動
                    elif key == self.test.getKeyValue('KEY_RIGHT') :  # 右
                        self.test.rightMove('40')                     # 右へ移動
                # end if
                elif key == self.test.getKeyValue('KEY_UP_EX'):
                    self.test.forwordMove('40')
                elif key == self.test.getKeyValue('KEY_DOWN_EX'):
                    self.test.backMove('40') 
                elif key == self.test.getKeyValue('KEY_LEFT_EX'):
                    self.test.leftMove('40')
                elif key == self.test.getKeyValue('KEY_RIGHT_EX'):
                    self.test.rightMove('40')    
            #end if
        # end while
        if self.cameraFlg is 1:                 
            self.test.endCameraThread()          # カメラモードオフ
            self.test.releaseCamera()            # カメラ設定開放

        self.test.end()                          # 自動着陸&ソケット閉じる
        print('終了')
    
if __name__ == "__main__":
    # TODO メイン
    test = telloClass(1)
    test.exe()