import librosa
import librosa.display
import matplotlib.pyplot as plt

y, sr = librosa.load('./voice/test1.wav')
plt.figure(figsize=(14, 5))
librosa.display.waveshow(y,alpha=0.4)
plt.show()
