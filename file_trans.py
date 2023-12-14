import librosa
import soundfile as sf

# 오디오 파일 로드
y, sr = librosa.load('./voice/그대만있다면.mp3')

# 옥타브 조절: 1 옥타브 올리기
y_shifted = librosa.effects.pitch_shift(y,n_steps=12, sr=sr)

# # 옥타브 조절: 1 옥타브 내리기
# y_shifted = librosa.effects.pitch_shift(y, sr, n_steps=-12)

# 조정된 오디오를 새로운 파일로 저장
sf.write('./voice/그대만있다면_+1.mp3', y_shifted, sr)
