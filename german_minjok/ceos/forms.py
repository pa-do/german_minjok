from django import forms
from .models import Store, StoreMenu

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['store_name', 'store_phone', 'store_number',
         'store_location', 'store_cartegory', 'store_image']
        labels = {'store_name': '가게 이름', 'store_phone': '가게 전화번호', 'store_number': '사업자 등록번호',
         'store_location': '가게 위치', 'store_cartegory': '업종', 'store_image': '가게 대표 이미지'}
         
    def __init__(self, *args, **kwargs):
        super(StoreForm, self).__init__(*args, **kwargs)
        self.fields['store_image'].required = False

class MenuForm(forms.ModelForm):
    class Meta:
        model = StoreMenu
        fields = ['menu_name', 'menu_info',
        'menu_price', 'menu_image']
        labels = {'menu_name': '메뉴 이름', 'menu_info': '메뉴 정보',
        'menu_price': '메뉴 가격', 'menu_image': '메뉴 이미지'}
         
    def __init__(self, *args, **kwargs):
        super(MenuForm, self).__init__(*args, **kwargs)
        self.fields['menu_image'].required = False