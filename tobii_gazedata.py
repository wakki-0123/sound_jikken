import tobii_research as tr
import time
import keyboard
import csv
# アイトラッカー動作時間
waittime = 5

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

keyboard.add_hotkey('s', toggle_streaming)

# キーボード入力を監視
keyboard.wait()
