import tobii_research as tr
import os
import time
import xml.etree.ElementTree as ET

found_eyetrackers = tr.find_all_eyetrackers()
my_eyetracker = found_eyetrackers[0]
gaze_data_list = [] # 視線データを格納するリスト


def gaze_data_callback(gaze_data): 
    gaze_data_list.append(gaze_data)



# キャリブレーションデータXMLファイルから読み込む
calibration_data_file_path = "C:/Users/Yoshiki Yasuda/Documents/Tobii Pro Lab/Project2/Data/Calibrations/2t0ylUIZtUuupVCckX7hSA.xml"

# XMLファイルを解析してキャリブレーションデータを取得
try:
    with open(calibration_data_file_path, "rb") as f:
        calibration_data = f.read()
except FileNotFoundError:
    print("Error: File not found.")
    exit()
except Exception as e:
    print(f"An error occurred while reading the file: {e}")
    exit()

# アイトラッカーにキャリブレーションデータを適用する
try:
    my_eyetracker.apply_calibration_data(calibration_data)
    print("Calibration data applied successfully.")
except Exception as e:
    print(f"An error occurred: {e}")

my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)
time.sleep(10)
my_eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)