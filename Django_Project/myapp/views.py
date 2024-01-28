from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.conf import settings
from .utils import handle_uploaded_file, calculate_frequency_range
from .models import FrequencyRange
from .forms import Uploadfileform
import numpy as np
import librosa
import os
import logging

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

    if f.name == "recorded_audio.ogg":
        FrequencyRange.objects.create(key=key)
    else:
        FrequencyRange.objects.create(file_name=f.name, key=key)

    request.session['key'] = key
    request.session['file_name'] = f.name if f.name != "recorded_audio.ogg" else None
    return f.name, key

def handle_audio_data(audio_data):
    try:
        file_name = 'recorded_audio.wav'
        file_path = os.path.join(settings.BASE_DIR, file_name)
        with open(file_path, 'wb') as f:
            f.write(audio_data)
        key = calculate_key(file_path)
    except Exception as e:
        logging.error(f"Error while handling audio data: {e}")
        key = None
    return key

def range(request):
    key = None
    file_name = None
    if request.method == "POST":
        form = Uploadfileform(request.POST, request.FILES)
        if form.is_valid():
            if 'file' in request.FILES:
                file_name, key = handle_uploaded_file(request.FILES['file'], request)
                request.session['viewed'] = False
            elif 'audio' in request.FILES:
                file_name, key = handle_uploaded_file(request.FILES['audio'], request)
                request.session['key'] = key
                request.session['file_name'] = file_name
            else:
                logging.warning("Form is not valid")
            return JsonResponse({'key':key, 'file_name':file_name})
        else:
            logging.warning("Form is not valid")
    else:
        form = Uploadfileform()
        key = request.session.get('key')
        file_name = request.session.get('file_name')
        viewed = request.session.get('viewed',True)
        if viewed:
            if key is not None and file_name is not None:
                del request.session['key']
                del request.session['file_name']
            return render(request, 'myapp/range.html', {'form':form})
        else:
            request.session['viewed'] = True
    return render(request, 'myapp/range.html', {'form': form, 'key': key,'file_name':file_name})