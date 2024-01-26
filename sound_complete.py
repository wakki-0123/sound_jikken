import pyautogui
import time
from psychopy import visual, core, sound
import os
import glob
import csv
from threading import Thread
import pyglet
import keyboard


#######################################################################################################
# 2台のモニターを使えるようになった
# パソコンのモニターには、vscodeを表示させておく
# 被験者の目の前のモニターには、グレースケール画像を表示させる(本プログラムにおいて指定する)
# 実験者の目の前のモニターには、実際にクリックできるよう脳波計、アイトラッカー、心拍計の画面を表示させておく(ドラック操作で移動させておくこと)
# また、音刺激を開始した時刻とファイル名をcsvファイルに記録するようにしている
# csvファイルに関しては，time_log_voice.csvというファイル名で作成される。また，ファイル名は任意に変更してよい。ただし，拡張子は.csvにすること
# csvファイルは記録したら逐次，保存 OR 削除すること．そうしないと元のcsvファイルに新たに書き込みされてしまう
# csvのファイル書き込みと音声の再生を終えるときは、キーボードのcを長押しする。また、コマンドライン上にEnd_Play_Soundと表示されたら音声刺激の再生が終了したことを示す。
# プログラムの終了は，コントロールキーとcを同時に押す


#######################################################################################################


# クリックする関数(ただし，心拍系だけダブルクリックじゃないと動かない)
def click2(position, position1, position2):
    x, y = position # アイトラッカーの座標
    x1, y1 = position1 # 脳波計
    x2, y2 = position2 # 心拍計
    pyautogui.click(x, y) 
    time.sleep(0.001)  # delayは0.001秒
    pyautogui.click(x1, y1)
    time.sleep(0.001)  # delayは0.001秒
    pyautogui.doubleClick(x2, y2)

# 音声ファイルの検索
def sound_load():
    # 音声ファイルのパスを指定
    cwd = os.getcwd()  # 現在の作業ディレクトリ
    sound_list = glob.glob(cwd + "/IADS-E sound stimuli (IADS-2 is not included)/Nature/*.wav") # 音声ファイルのパスを指定
    return sound_list


# 音声ファイルの読み込み
def sound_search(sound_list):
    sound_Data = {}
    filenames = []  # ファイル名を格納するリストを初期化
    for file_path in sound_list:
        sound_obj = pyglet.media.load(file_path)
        # ファイル名を取得し、辞書に追加
        filename = os.path.basename(file_path)
        sound_Data[filename] = sound_obj
    return sound_Data,filenames


    

# 音声ファイルの再生
def sound_play(sound_Data, time3, filenames):
    silent = "silent"
    print('音声再生開始時刻:', time3)
    time4 = time.perf_counter()
    write_to_csv(time3, "Start")  # 開始時刻をCSVに書き込み
    j = 0
    

    for filenames, sound_obj in sound_Data.items():
        # ここから音声の再生
        if j == 0:
          player = sound_obj.play()
          player.eos_action = pyglet.media.Player
          core.wait(6) # これがないと音声が再生されない
          player.pause()
          time5 = time.perf_counter()
          time6 = (time5 - time4) + time3
          print('音声再生終了時刻:', time6)
          print('音声再生終了ファイル:', filenames)  # 音声が終わったファイル名
          print(time6)
          write_to_csv(time6, filenames)  # 終了時刻とファイル名をCSVに書き込み
          
        else:
          # 無音声の再生
         
          core.wait(10) # 無音の再生(待機するだけ)
          time8 = time.perf_counter()
          
          time9 = (time8 - time4) + time3
          print('無音生終了時刻:', time9)
          print('無音生の文字列:', silent)  # 無音声を表す文字列を表示
          print(time9)
          write_to_csv(time9, silent)  # 終了時刻と無音声を表す文字列をCSVに書き込み
          ###############################################################

          # ここから音声の再生
          player = sound_obj.play()
          player.eos_action = pyglet.media.Player
          core.wait(6) # これがないと音声が再生されない
          player.pause()
          time5 = time.perf_counter()
          time6 = (time5 - time4) + time3
          print('音声再生終了時刻:', time6)
          print('音声再生終了ファイル:', filenames)  # 音声が終わったファイル名
          print(time6)
          write_to_csv(time6, filenames)  # 終了時刻とファイル名をCSVに書き込み

        # time6 = (time5 - time4) + time3
        # print('音声再生終了時刻:', time6)
        # print('音声再生終了ファイル:', filenames)  # 音声が終わったファイル名
        # print(time6)
        # write_to_csv(time6, filenames)  # 終了時刻とファイル名をCSVに書き込み
        j += 1
        
        # Check if 'c' key is pressed to break the loop (音声再生の強制終了)
        if keyboard.is_pressed('c'): # 音声の再生が終わったタイミングでキーボードのcを長押しすると音声再生が強制終了する
                print("End_Play_Sound")
                break
        
        #write_to_csv(time6, filename)  # 終了時刻とファイル名をCSVに書き込み
    



# CSVファイルに書き込み
def write_to_csv(time_value, filenames):
    with open('time_log_voice.csv', 'a', newline='', encoding='utf-8') as csvfile: # time_log_voice.csvは任意に変えてよい　ただし，拡張子は.csvにすること
        fieldnames = ['Timestamp', 'Name']  # 'Name'をfieldnamesに追加

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if csvfile.tell() == 0:
            writer.writeheader()

        writer.writerow({'Timestamp': time_value, 'Name': filenames})

#############################################################################################
# ここからメインプログラム

if __name__ == "__main__":

    # クリックしたい座標
    click_positions = [(657, 585)]  # アイトラッカー
    click_positions1 = [(1259, 64)]  # 脳波計
    click_positions2 = [(88, 90)]  # 心拍計

   
    sound_list = sound_load()

    # 以下，各デバイスによって，変更する(sound_device.pyを参照)

    # 使用したいサウンドデバイスを選択
    # selected_device = {
    #     'DeviceIndex': 7.0,
    #     'HostAudioAPIId': 13.0,
    #     'HostAudioAPIName': 'Windows WASAPI',
    #     'DeviceName': 'ヘッドホン (AVIOT TE-D01gv)',
    #     'NrInputChannels': 0.0,
    #     'NrOutputChannels': 2.0,
    #     'LowInputLatency': 0.0,
    #     'HighInputLatency': 0.0,
    #     'LowOutputLatency': 0.003,
    #     'HighOutputLatency': 0.01,
    #     'DefaultSampleRate': 44100.0,
    #     'id': 1
    # }
    #　使用したいサウンドデバイスを指定
    selected_device = {'DeviceIndex': 6.0,
                        'HostAudioAPIId': 13.0, 
                        'HostAudioAPIName': 'Windows WASAPI', 
                        'DeviceName': 'スピーカー (Realtek High Definition Audio)',
                          'NrInputChannels': 0.0,
                            'NrOutputChannels': 8.0,
                              'LowInputLatency': 0.0, 
                              'HighInputLatency': 0.0, 
                              'LowOutputLatency': 0.003, 
                              'HighOutputLatency': 0.0106667,
                                'DefaultSampleRate': 48000.0, 
                                'id': 1}
    sound_Data,filenames = sound_search(sound_list)
    click2(click_positions[0],click_positions1[0],click_positions2[0]) # 実際にクリックする 

    i = 0 # 経過時間のカウントのための変数
    # 経過時間の表示と音声の再生
    while True:
        i += 1
        if i == 1:#最初のループのみ time1に現在時刻を代入
            time1 = time.perf_counter()
        else: #2回目以降はtime1は固定する
            time1 = time1

        time.sleep(1) #1秒待つ
        time2 = time.perf_counter()
        print("経過時間:", time2 - time1) # 経過時間を表示
        time3 = time2 - time1 # 経過時間をtime3に代入

        if int(time3) == 3: # 3秒経過したら音を鳴らすようにする
            sound_thread = Thread(target=sound_play, args=(sound_Data,time3,filenames))
            

            sound_thread.start()
            
            
   
    