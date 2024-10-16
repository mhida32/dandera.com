from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, label="Имя пользователя")
    password = forms.CharField(widget=forms.PasswordInput,label="Пароль")

class RegistrationForm(forms.Form) :
    username = forms.CharField(max_length=50, label='Имя пользователя')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Потверждение пароля')