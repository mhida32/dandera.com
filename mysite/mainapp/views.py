from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginForm, RegistrationForm
import requests 

API_BASE_URL = "https://127.0.0.1:8001"


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            password_confirm = form.cleaned_data['password_confirm']
            
            if password != password_confirm:
                form.add_error('password_confirm','Пароли не совпадают')
            else:
                params = {
                    'username': username,
                    'password': password,
                    'role_name':'viewer'
                }

                response =  requests.post(f'{API_BASE_URL}/register/', params=params)
                
                if response.status_code == 200:
                    return redirect('login')
                else:
                    try:
                        error_detail = response.json().get('detail','')
                    except ValueError:
                        error_detail = 'Неизвестная ошибка'
                        
                    if isinstance(error_detail,list):
                        error_messages = []
                        for error in error_detail:
                            if 'msg' in error:
                                error_messages.append(error['msg'])
                            else:
                                error_messages.append(str(error))
                        error_detail ='; '.join(error_messages)
                    elif isinstance(error_detail, dict):
                        error_detail = error_detail.get('msg', str(error_detail))
                    else:
                        error_detail = str(error_detail)
                    
                    form.add_error(None,'Ошибка регистрации: ' + error_detail)
        else:
            pass
    else:
        form = RegistrationForm()
    return render(request,'mainapp/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.changed_data['username']
            password = form.changed_data['password']
            response = requests.post(f'{API_BASE_URL}/login/', auth=(username, password))
            
            if response.status_code == 200:
                request.session['username'] = username
                request.session['password'] = password
                return redirect('news_list')
            else:
                form.add_error(None,'Неверное имя пользователя или пароль')
    else:
        form = LoginForm()
    return render(request,'mainapp/login.html', {'form': form})






def logout_view(request):
    request.session.flush()
    return redirect('login')


def news_list_view(request):
    username = request.session.get('username')
    password = request.session.get('password')
    
    if not username or not password:
        return redirect('login')
    
    
    response = requests.get(f'{API_BASE_URL}/news/', auth=(username,password))
    
    if response.status_code == 200:
        new_list = response.json()
    else:
        news_list = []
        
    return render(request, 'mainapp/news_list.html', {'news_list': news_list})


def news_detail_view(request, news_id):
    username = request.session.get('username')
    password = request.session.get('password')
    
    if not username or not password:
        return redirect('login')
    
    
    response = requests.get(f'{API_BASE_URL}/news/{news_id}', auth=(username,password))
    
    if response.status_code == 200:
        news_item = response.json()
    else:
        news_item = None
        
        
    return render(request, 'mainapp/news_detail.html', {'news_items': news_item})