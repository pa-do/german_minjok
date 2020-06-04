import hashlib
import hmac
import base64
import requests
import time, json

from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from ceos.forms import StoreForm
from .models import UserLocation, UserPhoneCheck
from .forms import UserForm
from . import _keys


def signup_div(request):
    if request.user.is_authenticated:
        return redirect('main:index')
    if request.method == 'POST':
        user_code = request.POST.get('user-code')
        user_form = UserForm()
        if user_code == '소비자':
            context = {
                'user_code': user_code,
                'user_form': user_form,
            }
            return render(request, 'accounts/form.html', context)
        elif user_code == '판매자':
            context = {
                'user_code': user_code,
                'user_form': user_form,
            }
            return render(request, 'accounts/form.html', context)
        else:
            return redirect('accounts:div')
    else:
        return render(request, 'accounts/signup.html')


@require_POST
def signup(request):
    if request.user.is_authenticated:
        return redirect('main:index')
    user_code = request.POST.get('user_code')
    user_form = UserForm(request.POST)
    phone_number = request.POST.get('phone_number')
    roadAdr = request.POST.get('roadAddress')
    detailAdr = request.POST.get('detailAddress')
    if user_form.is_valid() and phone_number != '' and roadAdr != '' and detailAdr != '':
        user = user_form.save(commit=False)
        user.phone_number = phone_number
        if user_code == '소비자':
            user.auth_code = 1
        elif user_code == '판매자':
            user.auth_code = 2
        user.save()
        user_location = UserLocation()
        user_location.user = user
        user_location.location = roadAdr + ' ' + detailAdr
        user_location.location_basic = roadAdr
        user_location.location_detail = detailAdr
        user_location.save()
        auth_login(request, user)
        return redirect('main:index')
    context = {
        'user_code': user_code,
        'user_form': user_form,
    }
    return render(request, 'accounts/form.html', context)


def phone(request, phone_num):
    user_phone = UserPhoneCheck.objects.update_or_create(phone_number=phone_num)[0]
    timestamp = int(time.time() * 1000)
    timestamp = str(timestamp)

    url = "https://sens.apigw.ntruss.com"
    requestUrl = "/sms/v2/services/"
    requestUrl2 = "/messages"
    serviceId = _keys.serviceId
    access_key = _keys.access_key

    uri = requestUrl + serviceId + requestUrl2
    apiUrl = url + uri

    def make_signaure(uri, access_key):
        secret_key = _keys.secret_key
        secret_key = bytes(secret_key, 'UTF-8')
        method = "POST"
        message = method + " " + uri + "\n" + timestamp + "\n" + access_key
        message = bytes(message, 'UTF-8')
        signigKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
        return signigKey

    messages = { "to" : user_phone.phone_number }
    body = {
        "type" : "SMS",
        "contentType" : "COMM",
        "from" : "01076338540",
        "subject" : "subject",
        "content" : "[게르만 민족] 인증 번호 [{}]를 입력하세요.".format(user_phone.auth_number),
        "messages" : [messages]
    }
    body2 = json.dumps(body)
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "x-ncp-apigw-timestamp": timestamp,
        "x-ncp-iam-access-key": access_key,
        "x-ncp-apigw-signature-v2": make_signaure(uri, access_key)
    }

    res = requests.post(apiUrl, headers=headers, data=body2)
    print(res.json())
    context = {
        'message': 'OK',
    }
    return JsonResponse(context)


def phone_auth(request, phone_num, auth_num):
    result = UserPhoneCheck.objects.filter(
        phone_number=phone_num,
        auth_number=auth_num
    )
    message = 'fail'
    if result:
        message = 'success'
        result.delete()
    context = {
        'message': message
    }
    return JsonResponse(context)


def login(request):
    if request.user.is_authenticated:
        return redirect('main:index')
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('main:index')
    else:
        form = AuthenticationForm()
    context = {
        'form' : form
    }
    return render(request, 'accounts/login.html', context)


@login_required
def logout(request):
    auth_logout(request)
    return redirect('main:index')

