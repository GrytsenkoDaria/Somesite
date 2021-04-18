from django import forms
from .models import Product


class Productform(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'text', 'price', 'image', 'type']
        # изменить на ['name'], где в списке указываються поля модели

    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
