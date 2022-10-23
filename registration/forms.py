# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth import get_user_model
# from captcha.fields import CaptchaField
#
# User = get_user_model()
#
#
# class SignupForm(UserCreationForm):
#     email = forms.EmailField(max_length=200, widget=forms.EmailInput(attrs={'class': 'form-control'}))
#     captcha = CaptchaField()
#
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2', 'captcha')
#
#         widgets = {
#             'username': forms.TextInput(attrs={'class': 'form-control'}),
#         }

