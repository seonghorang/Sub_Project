from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings
from .utils import handle_uploaded_file, calculate_frequency_range
from .models import FrequencyRange
from .forms import Uploadfileform
import numpy as np
import librosa
import os

data_dir = os.path.join(settings.BASE_DIR, '..', 'data')

def index(request):
    return render(request, 'index.html')

def calculate_key(file_path):
    y, sr = librosa.load(file_path)
    # chroma feature 추출
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    # 각 chroma에 대한 평균 계산
    chroma_avg = np.mean(chroma, axis=1)
    # 가장 높은 값을 가진 chroma 찾기
    key_idx = np.argmax(chroma_avg)
    # chroma를 음계로 변환
    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    key = notes[key_idx]
    return key

def handle_uploaded_file(f, request):
    file_path = os.path.join(data_dir, f.name)
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    key = calculate_key(file_path)
    FrequencyRange.objects.create(file_name=f.name, key=key)
    request.session['key'] = key
    request.session['file_name'] = f.name
    return f.name, key

def range(request):
    file_name = None
    key = None
    if request.method == "POST":
        form = Uploadfileform(request.POST, request.FILES)
        if form.is_valid():
            file_name, key = handle_uploaded_file(request.FILES['file'], request)
            request.session['key'] = key
            return HttpResponseRedirect('/range')
    else:
        form = Uploadfileform()
    key = request.session.get('key', None)
    file_name = request.session.get('file_name', None)
    return render(request, 'myapp/range.html', {'form': form, 'key': key, 'file_name':file_name})