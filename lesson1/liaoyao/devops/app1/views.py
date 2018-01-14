from django.shortcuts import render
from django.http import JsonResponse

from .models import Book,Book2




def bookquery(request):
    data = [i for i in Book.objects.all().values('name','price')]
    return JsonResponse({'status':0,'data':data})
