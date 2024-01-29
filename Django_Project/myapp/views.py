from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.conf import settings
from .models import FrequencyRange
from .forms import Uploadfileform
import numpy as np
import librosa
import os
import logging

# 데이터가 저장될 디렉토리 경로 설정
data_dir = os.path.join(settings.BASE_DIR, '..', 'data')

# 메인 페이지를 렌더링하는 함수
def index(request):
    return render(request, 'index.html')

# 업로드된 오디오 파일의 키를 계산하는 함수
def calculate_key(file_path):
    # 오디오 파일 로드
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

# 업로드된 파일을 처리하는 함수
def handle_uploaded_file(f, request):
    # 파일 경로 설정
    file_path = os.path.join(data_dir, f.name)
    # 파일 저장
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    # 파일의 키 계산
    key = calculate_key(file_path)

    # 녹음된 오디오 파일인 경우와 아닌 경우에 따라 데이터베이스에 저장
    if f.name == "recorded_audio.ogg":
        FrequencyRange.objects.create(key=key)
    else:
        FrequencyRange.objects.create(file_name=f.name, key=key)
    
    # 세션에 키와 파일 이름 저장
    request.session['key'] = key
    request.session['file_name'] = f.name if f.name != "recorded_audio.ogg" else None
    return f.name, key

# 오디오 데이터를 처리하는 함수
def handle_audio_data(audio_data):
    try:
        # 파일 이름 설정
        file_name = 'recorded_audio.wav'
        file_path = os.path.join(settings.BASE_DIR, file_name)
        # 파일 저장
        with open(file_path, 'wb') as f:
            f.write(audio_data)
        # 파일의 키 계산
        key = calculate_key(file_path)
    except Exception as e:
        # 오류 로깅
        logging.error(f"Error while handling audio data: {e}")
        key = None
    return key

# 음역대 측정 페이지를 처리하는 함수
def range(request):
    key = None
    file_name = None
    if request.method == "POST":
        # POST 요청인 경우
        form = Uploadfileform(request.POST, request.FILES)
        if form.is_valid():
            # 폼 유효성 검사
            if 'file' in request.FILES:
                # 파일 업로드인 경우
                file_name, key = handle_uploaded_file(request.FILES['file'], request)
                request.session['viewed'] = False
            elif 'audio' in request.FILES:
                # 오디오 데이터인 경우
                file_name, key = handle_uploaded_file(request.FILES['audio'], request)
                request.session['key'] = key
                request.session['file_name'] = file_name
            else:
                logging.warning("Form is not valid")
            return JsonResponse({'key':key, 'file_name':file_name})
        else:
            logging.warning("Form is not valid")
    else:
        # GET 요청인 경우
        form = Uploadfileform()
        key = request.session.get('key')
        file_name = request.session.get('file_name')
        viewed = request.session.get('viewed',True)
        if viewed:
            if key is not None and file_name is not None:
                # 세션에서 키와 파일 이름 제거
                del request.session['key']
                del request.session['file_name']
            return render(request, 'myapp/range.html', {'form':form})
        else:
            request.session['viewed'] = True
    return render(request, 'myapp/range.html', {'form': form, 'key': key,'file_name':file_name})