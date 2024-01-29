from django.db import models

# FrequencyRange 모델 정의
class FrequencyRange(models.Model):
    # 파일 이름을 저장하는 CharField, 최대 길이는 200
    file_name = models.CharField(max_length=200)
    # 음의 키를 저장하는 CharField, 최대 길이는 2, 기본값은 'C'
    key = models.CharField(max_length=2, default='C')
