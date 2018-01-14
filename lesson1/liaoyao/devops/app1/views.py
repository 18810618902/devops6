from django.shortcuts import render
from django.http import JsonResponse,HttpResponse

from .models import Book,Book2,Author
from django.views import View
from django.views.generic import TemplateView,ListView


def bookquery(request):
    data = [i for i in Book.objects.all().values('name','price')]
    return JsonResponse({'status':0,'data':data})

def authorquery(request):
    qs = Author.objects.all()
    qsfans = qs.order_by('-fans')[:2]
    qsincome = qs.order_by('-income')[:2]
    qsret = list(set(qsfans).union(set(qsincome)))
    #data = [i.todict for i in Author.objects.all()]
    data = [i.todict for i in qsret]
    return JsonResponse({'status':0,'data':data})



class hello(View):
    def get(self,request):
        #print(request.method)
        return HttpResponse('hello world')


class authorlist(ListView):
    model = Author
    template_name = 'app1/authors.html'
    context_object_name = 'authors'
    paginate_by = 10

    def get_context_data(self,**kwargs):
        context = super(authorlist, self).get_context_data(**kwargs)
        context['job'] = 'pythoner'
        return context

    """
    def get_queryset(self):
        return self.model.objects.order_by('-name')
    """
