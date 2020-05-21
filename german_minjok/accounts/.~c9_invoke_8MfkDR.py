import requests
import time
from random import randint

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

from model_utils.models import TimeStampedModel


# Create your models here.
class User(AbstractUser):
    phone_number = models.CharField(max_length=20)
    auth_code = models.IntegerField()

class UserLocation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)



class UserPhoneCheck(TimeStampedModel):
    phone_number = models.CharField(verbose_name='휴대폰 번호', primary_key=True, max_length=11)
    auth_number = models.IntegerField(verbose_name='인증 번호')

    class Meta:
        db_table = 'auth'

    def save(self, *args, **kwargs):
        self.auth_number = randint(1000, 10000)
        super().save(*args, **kwargs)
        self.send_sms() # 인증번호가 담긴 SMS를 전송

    def make_signature(string):
        secret_key = bytes("발급받은 secret key를 넣어줍니다", 'UTF-8')
        string = bytes(string, 'UTF-8')
        string_hmac = hmac.new(secret_key, string, digestmod=hashlib.sha256).digest()
        string_base64 = base64.b64encode(string_hmac).decode('UTF-8')
        return string_base64

    def send_sms(self):
        url = 'https://api-sens.ncloud.com/v1/sms/services/ncp:sms:kr:259241911852:german_minjok_sms/messages/'
        data = {
            "type": "SMS",
            "from": "01076338540",
            "content": "[게르만 민족] 인증번호 [{}]를 입력해주세요.".format(self.auth_number),
            "messages":[{ "to": [self.phone_number],}]
        }
        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "x-ncp-apigw-timestamp" : timestamp
            "x-ncp-iam-access-key": MnYIs6OrJkEdFJcnsRm1,
            "x-ncp-service-secret": 64926d922e794cdfa350116de73d8af9,
        }
        requests.post(url, json=data, headers=headers)