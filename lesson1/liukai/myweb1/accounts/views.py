from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse

# Create your views here.


def userlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        print(username, password, user)
        if user:
            login(request, user)
            result = {'status': 0, 'error_message': ''}
        else:
            result = {'status': 1, 'error_message': 'username or password is error'}
        return JsonResponse(result)
    if request.method == 'GET':
        return render(request, 'pages/examples/login.html')


def userlogout(request):
    logout(request)
    return render(request, 'pages/examples/login.html')
