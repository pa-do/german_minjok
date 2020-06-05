from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
import requests
from carton.cart import Cart
from ceos.models import OrderList

# Create your views here.

def approval(request):
    order_list = OrderList.objects.filter(user=request.user).filter(order_condition=0)[0]   # 고쳐야함
    order_list.order_condition = 1
    order_list.save()

    cart = Cart(request.session)
    cart.clear()
    URL = 'https://kapi.kakao.com/v1/payment/approve'
    headers = {
        "Authorization": "KakaoAK " + "965c38ccc1d83d33c9577c0b870eb506",   # 변경불가
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8",  # 변경불가
    }
    User = get_user_model()
    user = get_object_or_404(User, pk=request.user.pk)
    params = {
        "cid": "TC0ONETIME",    # 변경불가. 실제로 사용하려면 카카오와 가맹을 맺어야함. 현재 코드는 테스트용 코드
        "tid": request.session['tid'],  # 결제 요청시 세션에 저장한 tid
        "partner_order_id": request.session['order_id'],     # 주문번호
        "partner_user_id": "{}".format(user),    # 유저 아이디
        "pg_token": request.GET.get("pg_token"),     # 쿼리 스트링으로 받은 pg토큰
    }

    res = requests.post(URL, headers=headers, params=params)
    amount = res.json()['amount']['total']
    res = res.json()
    context = {
        'res': res,
        'amount': amount,
    }
    return render(request, 'kakaopay/approval.html', context)

def cancel(request):
    return render(request, 'kakaopay/cancel.html')

def fail(request):
    return render(request, 'kakaopay/fail.html')
