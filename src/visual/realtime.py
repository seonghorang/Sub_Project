import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import queue

# 샘플링 속도 및 샘플링 할 시간 설정
fs = 44100
duration = 10  # seconds

# 실시간 그래프를 그리기 위한 설정
q = queue.Queue()

# 콜백 함수 정의
def callback(indata, frames, time, status):
    q.put(indata.copy())

# 마이크 입력 스트림 열기
stream = sd.InputStream(callback=callback, channels=1, samplerate=fs)
with stream:
    sd.sleep(duration * 1000)  # Wait for the stream to get some input data

while True:  # Now we draw the graph
    try:
        data = q.get_nowait()
        plt.plot(data)
        plt.pause(0.01)
        plt.cla()
    except queue.Empty:
        break
