import librosa
import numpy as np

# 오디오 파일 로드
y, sr = librosa.load('./voice/그대만있다면.mp3')

# 피치 추적
pitches, magnitudes = librosa.piptrack(y=y, sr=sr)

# 가장 높은 세기를 가진 피치 찾기
max_magnitude_index = np.unravel_index(magnitudes.argmax(), magnitudes.shape)
pitch = pitches[max_magnitude_index]

# 피치를 옥타브로 변환
octave = librosa.hz_to_octs(pitch)

print("노래의 키는 다음과 같습니다: ", octave)