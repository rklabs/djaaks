from django.conf.urls import url
from djview import views

urlpatterns = [
    url(r'^$', views.djview_index, name='djview_index'),
    url(r'^about/', views.djview_about, name='djview_about'),
    url(r'^add_category/', views.add_category, name='add_category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category,
        name='category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$',
        views.add_page,
        name='add_page'),
    url(r'^restricted/$', views.restricted, name='restricted'),
    # url(r'^register/$', views.register, name='register'),
    # url(r'^login/$', views.user_login, name='user_login'),
    # url(r'^logout/$', views.user_logout, name="user_logout")
]
