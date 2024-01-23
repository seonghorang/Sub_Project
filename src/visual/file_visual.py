import librosa
import librosa.display
import matplotlib.pyplot as plt

y, sr = librosa.load('./voice/그대만있다면.mp3')
plt.figure(figsize=(14, 5))
librosa.display.waveshow(y,alpha=0.4)
plt.show()
