from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="نام کاربری",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام کاربری'})
    )
    
    password1 = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز عبور'})
    )
    
    password2 = forms.CharField(
        label="تکرار رمز عبور",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'تکرار رمز عبور'})
    )
    
    first_name = forms.CharField(
        label="نام",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام'})
    )
    
    last_name = forms.CharField(
        label="نام خانوادگی",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام خانوادگی'})
    )
    
    email = forms.EmailField(
        label="ایمیل",
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('این ایمیل قبلا ثبت شده است.')
        return email 