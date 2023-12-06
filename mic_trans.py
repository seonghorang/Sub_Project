import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt

# 마이크 입력 설정
duration = 5  # 5초
fs = 44100  # Sample rate
samples = duration * fs

# 녹음 시작
myrecording = sd.rec(int(samples), samplerate=fs, channels=2)
sd.wait()  # 녹음이 끝날 때까지 기다림

# 그래프 그리기
plt.figure(figsize=(14, 5))
plt.plot(myrecording)
plt.show()
