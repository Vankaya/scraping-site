import codecs
import os, sys

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

import django
django.setup()
from django.db import DatabaseError

from scraping.work import *
from scraping.models import Vacancy, City, Language

parsers = (
    (work, 'https://www.work.ua/ru/jobs-python/'),
    (rabota, 'https://rabota.ua/zapros/python-developer/%d1%83%d0%ba%d1%80%d0%b0%d0%b8%d0%bd%d0%b0')
)

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

# h = codecs.open('work.txt', 'w', 'utf-8')
# h.write(str(jobs))
# h.close()