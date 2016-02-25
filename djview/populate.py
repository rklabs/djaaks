import os

from models import Category
from models import Page

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 
                      'djaaks.settings')
django.setup()

def add_category(name):
    category = Category.objects.get_or_create(name=name)[0]
    category.save()

    return category

def add_page(category, title, url, views=0):
    page = Page.objects.get_or_create(category=category,
                                      title=title)[0]
    page.url = url
    page.views = views
    page.save()

    return page

def populate():
    pycat = add_category('Python')

    add_page(category=pycat,
             title='Official Python Tutorial',
             url='http://www.greenteapress.com/thinkpython/')

    add_page(category=pycat,
             title='Learn Python in 10 Minutes',
             url='http://www.korokithakis.net/tutorials/python/')

    djcat = add_category('Django')

    add_page(category=djcat,
             title='How to Tango with Django',
             url='https://docs.djangoproject.com/en/1.5/intro/tutorial01/')

    othercat = add_category('Other')

    add_page(category=othercat,
             title='Bottle',
             url='http://bottlepy.org/docs/dev/')

    add_page(category=othercat,
             title='Flask',
             url='http://flask.pocoo.org')

