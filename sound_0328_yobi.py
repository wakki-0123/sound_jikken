import pyautogui
import time
import os
import glob
import csv
from psychopy import core
import keyboard
import pyglet

# Function to click on specified positions
def click2(position, position1, position2):
    x, y = position
    x1, y1 = position1
    x2, y2 = position2
    pyautogui.click(x, y)
    time.sleep(0.001)
    pyautogui.click(x1, y1)
    time.sleep(0.001)
    pyautogui.doubleClick(x2, y2)

# Function to load sound files
def sound_load(folder_path):
    sound_list = glob.glob(os.path.join(folder_path, "*.wav"))
    return sound_list

# Function to play sounds using Pyglet
def sound_play(sound_list, time3):
    time4 = time.perf_counter()
    j = 0

    for sound_file in sound_list:
        filename = os.path.basename(sound_file)

        player = pyglet.media.Player()
        sound = pyglet.media.load(sound_file)
        player.queue(sound)
        player.play()

        time5 = time.perf_counter()
        time6 = (time5 - time4) + time3
        print('音声再生開始時刻:', time6)
        print('音声再生ファイル:', filename)  

        # Wait for the sound to finish playing
        player.push_handlers(on_eos=lambda: pyglet.app.exit())
        pyglet.app.run()

        time5 = time.perf_counter()
        time6 = (time5 - time4) + time3
        print('音声再生終了時刻:', time6)
        print('音声再生終了ファイル:', filename)  

        # 再度同じ音を再生する前に5秒待機
        time.sleep(5)

        # 再度同じ音を再生
        player = pyglet.media.Player()
        sound = pyglet.media.load(sound_file)
        player.queue(sound)
        player.play()
        time5 = time.perf_counter()
        time6 = (time5 - time4) + time3
        print('音声再生開始時刻:', time6)
        print('音声再生ファイル:', filename)

        # Wait for the sound to finish playing
        player.push_handlers(on_eos=lambda: pyglet.app.exit())
        pyglet.app.run()
        time5 = time.perf_counter()
        time6 = (time5 - time4) + time3
        print('音声再生開始時刻:', time6)
        print('音声再生ファイル:', filename)

        # インターバルを設定
        time.sleep(10)

        j += 1

    return j

# Function to write to CSV
def write_to_csv(time_value, filenames):
    with open('time_log_voice.csv', 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Timestamp', 'Name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if csvfile.tell() == 0:
            writer.writeheader()

        writer.writerow({'Timestamp': time_value, 'Name': filenames})

if __name__ == "__main__":
    click_positions = [(657, 585)]
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
    

    sound_folder = "sound_jikken1/実験で使う音刺激(候補)/ニュートラル"
    sound_folder1 = "sound_jikken1/実験で使う音刺激(候補)/ネガティブ"
    sound_folder2 = "sound_jikken1/実験で使う音刺激(候補)/ポジティブ"

    sound_list = sound_load(sound_folder)
    sound_list1 = sound_load(sound_folder1)
    sound_list2 = sound_load(sound_folder2)

    p = len(sound_list)
    q = len(sound_list1)
    r = len(sound_list2)


    click2(click_positions[0], click_positions1[0], click_positions2[0])
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

