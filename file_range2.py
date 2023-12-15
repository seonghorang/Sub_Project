import librosa
import numpy as np

# 오디오 파일 로드
y, sr = librosa.load('./voice/좋아해_-0.5.mp3')

# chroma feature 추출
chroma = librosa.feature.chroma_cqt(y=y, sr=sr)

# 각 chroma에 대한 평균 계산
chroma_avg = np.mean(chroma, axis=1)

# 가장 높은 값을 가진 chroma 찾기
key_idx = np.argmax(chroma_avg)

# chroma를 음계로 변환
notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
key = notes[key_idx]

print("노래의 키는 다음과 같습니다: ", key)
