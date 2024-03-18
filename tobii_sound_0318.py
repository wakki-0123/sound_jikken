import threading
import tobii_research as tr
import time
import keyboard
import csv
import pyautogui
import time
import os
import glob
from psychopy import core
import pyglet

# アイトラッカー動作時間
waittime = 40

# アイトラッカー検出
found_eyetrackers = tr.find_all_eyetrackers()
my_eyetracker = found_eyetrackers[0]
gaze_data_list = [] # 視線データを格納するリスト

def gaze_data_callback(gaze_data): 
    gaze_data_list.append(gaze_data)

# キーボードのsキーでストリーミングを開始/停止する
def toggle_streaming():
    my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)
    time.sleep(waittime)
    my_eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)
    # CSVファイルに視線データを書き込む
    with open('gaze_data.csv', 'w', newline='') as csvfile:
        fieldnames = ['Time_stamp','Left_eye_diameter', 'Right_eye_diameter']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in gaze_data_list:
            time_stamp = data['device_time_stamp']
            left_eye_diameter = data['left_pupil_diameter']
            right_eye_diameter = data['right_pupil_diameter']
            # csv書き込み
            writer.writerow({
                'Time_stamp': time_stamp,
                'Left_eye_diameter': left_eye_diameter,
                'Right_eye_diameter': right_eye_diameter
            })
            # gaze_data_list を別のファイルに書き込む
    with open('gaze_data_list.txt', 'w') as file:
     for data in gaze_data_list:
        file.write(f"{data}\n")

# Function to click on specified positions
def click2(position1, position2):
    
    x1, y1 = position1
    x2, y2 = position2
    
    pyautogui.click(x1, y1)
    time.sleep(0.001)
    pyautogui.doubleClick(x2, y2)

# Function to load sound files
def sound_load(folder_path):
    sound_list = glob.glob(os.path.join(folder_path, "*.wav"))
    return sound_list

# Function to play sounds using Pyglet
def sound_play(sound_list,time3):
    time4 = time.perf_counter()
    j = 0

    filename = []  # ファイル名を格納するリストを初期化
    for sound_file in sound_list:
        
        filename = os.path.basename(sound_file)
        
        player = pyglet.media.Player()
        sound = pyglet.media.load(sound_file)
        player.queue(sound)
        
        

        player.play()

        time5 = time.perf_counter()
        time6 = (time5 - time4) + time3
        write_to_csv(time6, "Start")
        player.on_eos = lambda: None  # Do nothing when the sound ends

        # Wait for the sound to finish playing
        player.push_handlers(on_eos=lambda: pyglet.app.exit())
        pyglet.app.run()
        j += 1
        time5 = time.perf_counter()
        time6 = (time5 - time4) + time3
        print('音声再生終了時刻:', time6)
        print('音声再生終了ファイル1:', filename)  # 音声が終わったファイル名
        print(time6)
        write_to_csv(time6, filename)  # 終了時刻とファイル名をCSVに書き込み
          

        # Pause for a moment before playing the next sound
        time.sleep(10)
        #time5 = time.perf_counter()

    return j

# Function to write to CSV
def write_to_csv(time_value, filenames):
    with open('time_log_voice.csv', 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Timestamp', 'Name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if csvfile.tell() == 0:
            writer.writeheader()

        writer.writerow({'Timestamp': time_value, 'Name': filenames})

def main_function():

    click_positions1 = [(1259, 64)]
    click_positions2 = [(120, 10)]

    # 使用したいサウンドデバイスを指定
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
    
    # キャリブレーションファイルをロード
    calibration_file = "my_calibration.cal"  # キャリブレーションファイルのパスを指定
    my_eyetracker.apply_calibration_data(calibration_file)

    sound_folder = "sound_jikken1/実験で使う音刺激(候補)/ニュートラル"
    sound_folder1 = "sound_jikken1/実験で使う音刺激(候補)/ネガティブ"
    sound_folder2 = "sound_jikken1/実験で使う音刺激(候補)/ポジティブ"

    sound_list = sound_load(sound_folder)
    sound_list1 = sound_load(sound_folder1)
    sound_list2 = sound_load(sound_folder2)

    p = len(sound_list)
    q = len(sound_list1)
    r = len(sound_list2)


    click2(click_positions1[0], click_positions2[0])
    time0 = time.perf_counter()

    i = 0
    
    j = 0 
    k = 0
    l = 0
    

    while True:
        i += 1
        if i == 1:
            time1 = time0
            
        else:
            time1 = time1

        
        time.sleep(1)
        time2 = time.perf_counter()
        time3 = time2 - time1
        print("経過時間:", time3)
        

        if int(time3) == 3:
           
            j = sound_play(sound_list,time3)
            # デバックしやすいように設定
            if keyboard.is_pressed('c'):
              print("End_Play_Sound")
              break
           

        if j == p:
            time8 = time.perf_counter()
            time8 = time8 - time1
           
            k = sound_play(sound_list1,time8)
            j = 0

        if k == q:
            time9 = time.perf_counter()
            time9 = time9 - time1
            l = sound_play(sound_list2,time9)
            k = 0

         # Check if 'c' key is pressed to break the loop
        if keyboard.is_pressed('c'):
            print("End_Play_Sound")
            break


# プログラムを終了するためのキーを監視するスレッド
def listen_for_exit():
    global exit_flag
    keyboard.wait('q')
    exit_flag = True

if __name__ == "__main__":
    exit_flag = False
    # スレッドのターゲットを定義する
    main_thread = threading.Thread(target=main_function)  # main_function を実際のメインロジックに置き換える
    exit_thread = threading.Thread(target=listen_for_exit)  # キーボード入力を監視するスレッド
    # 両方のスレッドを開始する
    main_thread.start()
    toggle_streaming()  # toggle_streaming 関数をメインスレッドで実行する
    exit_thread.start()
    # メインスレッドが終了フラグが True に設定されるまで待機
    while not exit_flag:
        time.sleep(1)
    print("Exiting the program...")
