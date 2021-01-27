from django.shortcuts import render
import time

from .forms import FindForm
from .models import Vacancy

def home_view(request):
    form = FindForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    print (city, language)
    qs = []
    if city or language:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        if language:
            _filter['language__slug'] = language
        qs = Vacancy.objects.filter(**_filter)
    return render(request, 'scraping/home.html', {'object_list': qs,
                                                  'form': form})


def test_rest(request):
    name = 'Ivan'
    return render(request, 'scraping/home.html', {'name': name})


