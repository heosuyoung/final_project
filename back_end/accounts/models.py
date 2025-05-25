from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    GENDER_CHOICES = (
        ('M', '남자'),
        ('F', '여자'),
        ('O', '기타'),
    )
    
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True,
    )
    
    # 추가 필드
    birth_date = models.CharField(max_length=8, blank=True, null=True, help_text='YYYYMMDD 형식')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        swappable = 'AUTH_USER_MODEL'  # 충돌 방지용
