from django.shortcuts import render, get_object_or_404, redirect
import requests
from django.http import JsonResponse

from carton.cart import Cart
from ceos.models import StoreMenu, Store


def menu(request, store_pk):
    store = get_object_or_404(Store, pk=store_pk)
    menu_list = store.storemenu_set.all()
    print(store, menu_list)
    context = {
        'menu_list': menu_list,
        'store': store,
    }
    return render(request, 'shopping/menu_list.html', context)


def add_product(request):
    cart = Cart(request.session)
    menu = get_object_or_404(StoreMenu, pk=request.GET.get('menu'))
    cart.add(menu, price=menu.menu_price)
    context = {
        'total': cart.total,
    }
    return JsonResponse(context)


def minus_product(request):
    cart = Cart(request.session)
    menu = get_object_or_404(StoreMenu, pk=request.GET.get('menu'))
    cart.remove_single(menu)
    context = {
        'total': cart.total,
    }
    return JsonResponse(context)


def show_cart(request):
    current_site = request.build_absolute_uri()[:-10]
    cart = Cart(request.session)
    cnt = 0
    cart_item = 'none'
    status = 0
    for item in cart.items:
        cnt += 1
        if cnt == 0:
            cart_item = '{}'.format(item.product.name)
            status = 1
    if cnt > 1:
        cart_item += '외 {}건'.format(cnt-1)

    if request.method == "POST":    # 버튼 누르면
        URL = 'https://kapi.kakao.com/v1/payment/ready'
        headers = {
            "Authorization": "KakaoAK " + "965c38ccc1d83d33c9577c0b870eb506",   # 변경불가
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",  # 변경불가
        }
        params = {
            "cid": "TC0ONETIME",    # 변경불가. 실제로 사용하려면 카카오와 가맹을 맺어야함. 현재 코드는 테스트용 코드
            "partner_order_id": "{}_{}".format(1, 1),     # 주문번호 (스토어 번호_주문 번호)
            "partner_user_id": "{}".format(request.user),    # 유저 아이디
            "item_name": "{}".format(cart_item),        # 구매 물품 이름
            "quantity": "{}".format(cnt),                # 구매 물품 수량
            "total_amount": "{}".format(1),        # 구매 물품 가격
            # "total_amount": "{}".format(cart.total),  # 구매 물품 가격
            "tax_free_amount": "0",         # 구매 물품 비과세 (0으로 고정)
            "approval_url": "{}kakaopay/approval/".format(current_site),    # 결제 성공 시 이동할 url
            "cancel_url": "{}kakaopay/cancel/".format(current_site),               # 결제 취소 시 이동할 url
            "fail_url": "{}kakaopay/fail/".format(current_site),                 # 결제 실패 시 이동할 url
        }

        res = requests.post(URL, headers=headers, params=params)
        request.session['tid'] = res.json()['tid']  # 결제 승인시 사용할 tid를 세션에 저장
        next_url = res.json()['next_redirect_pc_url']  # 결제 페이지로 넘어갈 url을 저장
        return redirect(next_url)

    context = {
        'status': status
    }

    return render(request, 'shopping/show_cart.html', context)