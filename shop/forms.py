from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from goods.models import Product, ProductImage


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field_names = [field_name for field_name, _ in self.fields.items()]
        for field_name in field_names:
            field = self.fields.get(field_name)
            field.widget.attrs.update({'placeholder': field.label})


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['category', 'sub_category', 'image', 'title', 'description', 'price', 'location', 'mobile_number']

class ProductImageForm(ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']