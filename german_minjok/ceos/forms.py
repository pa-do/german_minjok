from django import forms
from .models import Store

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