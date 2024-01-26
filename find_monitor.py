from psychopy import monitors

# 利用可能なスクリーンに関する情報を取得
screens = monitors.getAllMonitors()

# 各スクリーンに関する情報を表示
for screen in screens:
    print(screen)
