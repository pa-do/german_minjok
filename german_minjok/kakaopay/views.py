from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
import requests
from carton.cart import Cart
from ceos.models import StoreMenu, Store, OrderList
# Create your views here.

def approval(request):
    User = get_user_model()
    user = get_object_or_404(User, pk=request.user.pk)
    cart = Cart(request.session)
    order_items = []
    for item in cart.items:
        cart_item = item.product.menu_name
        cart_quantity = item.quantity
        order_items.append('{}_{}'.format(cart_item, cart_quantity))

    order_list = OrderList.objects.create(
        user=user,
        store=get_object_or_404(Store, pk=request.session['store_pk']),
        order_condition=1,
        order_location=request.COOKIES['adr'] + ' ' + request.COOKIES['dadr'],
        order_name='/'.join(order_items),  # 유저이름 + 가게이름: 의미 없는 문자열
        order_price=cart.total  # 장바구니의 총 가격
    )

    cart.clear()
    URL = 'https://kapi.kakao.com/v1/payment/approve'
    headers = {
        "Authorization": "KakaoAK " + "965c38ccc1d83d33c9577c0b870eb506",   # 변경불가
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8",  # 변경불가
    }
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
