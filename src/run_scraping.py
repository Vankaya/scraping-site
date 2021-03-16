import codecs
import os, sys

from django.contrib.auth import get_user_model

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

import django
django.setup()
from django.db import DatabaseError

from scraping.work import *
from scraping.models import Vacancy, City, Language, Error

User = get_user_model()

parsers = (
    (work, 'https://www.work.ua/ru/jobs-python/'),
    (rabota, 'https://rabota.ua/zapros/python-developer/%d1%83%d0%ba%d1%80%d0%b0%d0%b8%d0%bd%d0%b0')
)


def get_settings():
    qs = User.objects.filter(send_email=True).values()
    settings_lst = set((q['city_id'], q['language_id']) for q in qs)
    return  settings_lst

q = get_settings()

city = City.objects.filter(slug='kiev').first()
language = Language.objects.filter(slug='python').first()

jobs, errors = [], []
for func, url in parsers:
    j, e = func(url)
    jobs += j
    errors += e

for job in jobs:
    v = Vacancy(**job, city=city, language=language)
    try:
        v.save()
    except DatabaseError:
        pass
if errors:
    er = Error(data=errors).save()

# h = codecs.open('work.txt', 'w', 'utf-8')
# h.write(str(jobs))
# h.close()