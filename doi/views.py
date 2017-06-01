from django.shortcuts import render
from .models import *

def homepage(request):
    count = Article.objects.count()
    article = Article.objects.order_by('?').first()
    return render(request, 'homepage.html', {
        'article': article,
    })
