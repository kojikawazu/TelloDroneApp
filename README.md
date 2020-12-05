★Telloを使用したドローンアプリ制御★

ドローンをパソコンから制御するアプリを作りました。
カメラ取得、MissionPad検出も可能です。

言語: Python
ライブラリ: Tello, OpenCV

フォルダ: practice, lib_exe

〇practice(教育用)

# ドローンを離陸させて上下左右に移動するアプリ
tello_first.py

# ドローンを離陸させて、受信スレッドを動作するアプリ
tello_recv.py  　

# ドローンのカメラをキャプチャーして、画面に出力するアプリ
tello_camera.py

# ドローンのビジョンポジショニングシステムを利用してMissionPadを検出し
# ドローンを制御するアプリ。
tello_pad.py

# パソコンのカメラをキャプチャーして、画面に出力するアプリ
cv2_camera_test.py


〇lib_exe

# Telloの制御を纏めた自作ライブラリ
libtello.py

# ドローンのカメラキャプチャー機能＋キーボード制御機能を搭載したアプリ
tello_key.py

# ドローンのカメラをキャプチャーして、画面に出力するアプリ
tello_camera.py

# ドローンのビジョンポジショニングシステムを利用してMissionPadを検出し
# ドローンを制御するアプリ。
tello_mission.py
