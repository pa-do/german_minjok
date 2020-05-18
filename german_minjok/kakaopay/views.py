from django.shortcuts import render, redirect
import requests

# Create your views here.
def index(request):
    if request.method == "POST":
        URL = 'https://kapi.kakao.com/v1/payment/ready'
        headers = {
            "Authorization": "KakaoAK " + "965c38ccc1d83d33c9577c0b870eb506",   # 변경불가
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",  # 변경불가
        }
        params = {
            "cid": "TC0ONETIME",    # 변경불가. 실제로 사용하려면 카카오와 가맹을 맺어야함. 현재 코드는 테스트용 코드
            "partner_order_id": "1001",     # 주문번호
            "partner_user_id": "german",    # 유저 아이디
            "item_name": "연어초밥",        # 구매 물품 이름
            "quantity": "1",                # 구매 물품 수량
            "total_amount": "12000",        # 구매 물품 가격
            "tax_free_amount": "0",         # 구매 물품 비과세 (0으로 고정)
            "approval_url": "http://127.0.0.1:8080/kakaopay/approval",    # 결제 성공 시 이동할 url
            "cancel_url": "http://127.0.0.1:8080/kakaopay/cancel/",               # 결제 취소 시 이동할 url
            "fail_url": "http://127.0.0.1:8080/kakaopay/fail/",                 # 결제 실패 시 이동할 url
        }

        res = requests.post(URL, headers=headers, params=params)
        request.session['tid'] = res.json()['tid']      # 결제 승인시 사용할 tid를 세션에 저장
        next_url = res.json()['next_redirect_pc_url']   # 결제 페이지로 넘어갈 url을 저장
        return redirect(next_url)


    return render(request, 'kakaopay/index.html')


def approval(request):
    URL = 'https://kapi.kakao.com/v1/payment/approve'
    headers = {
        "Authorization": "KakaoAK " + "965c38ccc1d83d33c9577c0b870eb506",   # 변경불가
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8",  # 변경불가
    }
    params = {
        "cid": "TC0ONETIME",    # 변경불가. 실제로 사용하려면 카카오와 가맹을 맺어야함. 현재 코드는 테스트용 코드
        "tid": request.session['tid'],  # 결제 요청시 세션에 저장한 tid
        "partner_order_id": "1001",     # 주문번호
        "partner_user_id": "german",    # 유저 아이디
        "pg_token": request.GET.get("pg_token"),     # 쿼리 스트링으로 받은 pg토큰
    }

    res = requests.post(URL, headers=headers, params=params)
    print('여기->', res.json())
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