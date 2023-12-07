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


##### 마이크 입력 후 시각화
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt

# 샘플링 레이트
sr = 22050

# 녹음 시간
duration = 5  # seconds

# 녹음 시작
recording = sd.rec(int(duration * sr), samplerate=sr, channels=1)
sd.wait()  # Wait until the recording is done

# 녹음된 데이터 시각화
plt.plot(recording)
plt.show()