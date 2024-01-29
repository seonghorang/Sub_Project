import librosa
import os

# 업로드된 파일을 처리하는 함수
def handle_uploaded_file(f):
    # 현재 파일의 기본 디렉토리 설정
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # 데이터를 저장할 디렉토리 경로 설정
    data_dir = os.path.join(base_dir, '../../data')

    # 데이터 디렉토리가 없으면 생성
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    # 파일 경로 설정
    file_path = os.path.join(data_dir, f.name)
    # 파일 저장
    with open(file_path,'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    # 오디오 파일 로드
    y, sr = librosa.load(file_path)
    # 스펙트럼 대비 계산
    spectral_contrast = librosa.feature.spectral_contrast(y=y,sr=sr)

    return spectral_contrast

# 파일의 주파수 범위를 계산하는 함수
def calculate_frequency_range(file_path):
    # 오디오 파일 로드
    y, sr = librosa.load(file_path)
    # 스펙트럼 중심 계산
    spectral_centroids = librosa.feature.spectral_centroid(y, sr=sr)[0]
    # 주파수 범위 반환
    return min(spectral_centroids), max(spectral_centroids)