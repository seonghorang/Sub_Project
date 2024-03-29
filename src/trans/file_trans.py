import librosa
import soundfile as sf

# 오디오 파일 로드
y, sr = librosa.load('./voice/첫눈처럼.mp3')

# # 옥타브 조절: 1 옥타브 올리기
# y_shifted = librosa.effects.pitch_shift(y,n_steps=12, sr=sr)

# 옥타브 조절: 1 옥타브 내리기
y_shifted = librosa.effects.pitch_shift(y, n_steps=-3, sr=sr)

# 조정된 오디오를 새로운 파일로 저장
sf.write('./voice/첫눈처럼_-3.mp3', y_shifted, sr)
