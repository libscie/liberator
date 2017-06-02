from django.shortcuts import render
from .models import *

def homepage(request):
    count = Article.objects.count()
    missing = Article.objects.filter(has_been_uploaded = False).count()
    costs = missing * 30
    article = Article.objects.order_by('?').first()
    return render(request, 'homepage.html', {
        'count': count,
        'article': article,
        'missing': missing,
        'costs': costs
    })
