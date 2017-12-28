#encoding: utf-8
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    return render(request,'index.html')


def needlogin(request):
    print(request.POST)
    if request.method == 'GET':
        return render(request, 'pages/examples/login.html')
    if request.method == 'POST':
        name = request.POST.get('name')
        pwd = request.POST.get('pwd')
        user = authenticate(username=name,password=pwd)
        result = {}
        if user:
            login(request,user)
            result['status'] = 0
            #return HttpResponseRedirect('/')
        else:
            result['status'] = 1
        return JsonResponse(result)



def test(request):
    print(request.POST)
    if request.method == 'GET':
        return render(request, 'test.html')
    if request.method == 'POST':
        name = request.POST.get('name')
        pwd = request.POST.get('pwd')
        result = {name: pwd}
        return JsonResponse(result)
