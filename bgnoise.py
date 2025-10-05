import threading
import sounddevice as sd
import numpy as np
import pystray
from PIL import Image, ImageDraw
import tkinter as tk

# 参数
duration = 1.0
sample_rate = 44100
volume = 0.005  # 初始音量

playing = False
stop_thread = False

# 创建托盘图标
def create_image():
    image = Image.new('RGB', (64, 64), color='white')
    d = ImageDraw.Draw(image)
    d.rectangle([16, 16, 48, 48], fill='black')
    return image

# 底噪播放线程
def play_noise():
    global playing, volume
    while not stop_thread:
        if playing:
            noise = np.random.uniform(-1, 1, int(sample_rate * duration)) * volume
            sd.play(noise, samplerate=sample_rate, blocking=True)
        else:
            sd.sleep(500)

# 托盘菜单操作
def toggle_noise(icon, item):
    global playing
    playing = not playing
    item.text = "停止底噪" if playing else "开启底噪"

def quit_app(icon, item):
    global stop_thread
    stop_thread = True
    icon.stop()

def adjust_volume(icon, item):
    # 弹出滑块窗口
    def on_slide(val):
        global volume
        volume = float(val)

    window = tk.Tk()
    window.title("底噪音量")
    window.geometry("300x100")
    slider = tk.Scale(window, from_=0.0, to=0.02, resolution=0.0005,
                      orient=tk.HORIZONTAL, label="音量", command=on_slide)
    slider.set(volume)
    slider.pack(fill=tk.X, padx=20, pady=20)
    window.mainloop()

# 启动播放线程
thread = threading.Thread(target=play_noise, daemon=True)
thread.start()

# 创建托盘图标
icon = pystray.Icon("底噪", create_image(), "底噪控制",
                    menu=pystray.Menu(
                        pystray.MenuItem("开启底噪", toggle_noise),
                        pystray.MenuItem("调整音量", adjust_volume),
                        pystray.MenuItem("退出", quit_app)
                    ))
icon.run()
