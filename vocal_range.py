import numpy as np
import sounddevice as sd
import librosa

# 샘플링 레이트
sr = 22050

# 녹음 시간
duration = 5  # seconds

# 녹음 시작
recording = sd.rec(int(duration * sr), samplerate=sr, channels=1)
sd.wait()  # Wait until the recording is done

# 음역대 분석
S = librosa.stft(recording.flatten())
Sdb = librosa.amplitude_to_db(abs(S), ref=np.max, amin=1e-5)  # Set amin parameter

# 음역대 출력
frequencies = librosa.fft_frequencies(sr=sr, n_fft=S.shape[0])

# 사용자 음역대 평균 dB 계산
user_freq_range = (85, 255)  # User's frequency range in Hz
user_freq_indices = np.where((frequencies >= user_freq_range[0]) & (frequencies <= user_freq_range[1]))[0]
user_freq_avg_db = Sdb[user_freq_indices].mean()

# 사용자 음역대를 옥타브로 변환
user_octave = librosa.hz_to_octs(frequencies[user_freq_indices])

# 옥타브를 주파수로 변환
user_freq = librosa.octs_to_hz(user_octave)

# 주파수를 MIDI 번호로 변환
user_midi = librosa.hz_to_midi(user_freq)

# MIDI 번호를 음이름과 옥타브 번호로 변환
lowest_note = librosa.midi_to_note(np.round(user_midi.min()))
highest_note = librosa.midi_to_note(np.round(user_midi.max()))

print(f"당신의 목소리에서 가장 낮은 음은 {lowest_note}, 가장 높은 음은 {highest_note}입니다.")
