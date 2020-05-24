from django import forms
from .models import Store

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['store_name', 'store_phone', 'store_number',
         'store_location', 'store_cartegory', 'store_image']
    
    def __init__(self, *args, **kwargs):
        super(StoreForm, self).__init__(*args, **kwargs)
        self.fields['store_image'].required = False