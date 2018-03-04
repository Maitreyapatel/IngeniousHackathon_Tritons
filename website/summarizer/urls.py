from django.conf.urls import url,include
from . import views

urlpatterns = [
    url(r'^/app$',views.appsum,name='app'),
    #url(r'^$',views.index,name='index'),
]
