★Telloを使用したドローンアプリ制御★

ドローンをパソコンから制御するアプリを作りました。
カメラ取得、MissionPad検出も可能です。

言語: Python
ライブラリ: Tello, OpenCV

フォルダ: practice, lib_exe

〇practice(教育用)

tello_first.py   　　# ドローンを離陸させて上下左右に移動するアプリ
tello_recv.py    　　# ドローンを離陸させて、受信スレッドを動作するアプリ
tello_camera.py  　　# ドローンのカメラをキャプチャーして、画面に出力するアプリ
tello_pad.py     　　# ドローンのビジョンポジショニングシステムを利用してMissionPadを検出し
　　　　　　　　　　　 # ドローンを制御するアプリ。
cv2_camera_test.py　 # パソコンのカメラをキャプチャーして、画面に出力するアプリ


〇lib_exe

libtello.py          # Telloの制御を纏めた自作ライブラリ
tello_key.py         # ドローンのカメラキャプチャー機能＋キーボード制御機能を搭載したアプリ
tello_camera.py      # ドローンのカメラをキャプチャーして、画面に出力するアプリ
tello_mission.py     # ドローンのビジョンポジショニングシステムを利用してMissionPadを検出し
　　　　　　　　　　　 # ドローンを制御するアプリ。





