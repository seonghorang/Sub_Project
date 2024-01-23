import librosa
import os

def handle_uploaded_file(f):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, '../../data')

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    file_path = os.path.join(data_dir, f.name)
    with open(file_path,'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    y, sr = librosa.load(file_path)

    spectral_contrast = librosa.feature.spectral_contrast(y=y,sr=sr)

    return spectral_contrast