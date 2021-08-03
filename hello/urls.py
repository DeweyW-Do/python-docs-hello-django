
from django.urls import path, include
from django.conf.urls import url
from . import views
 
urlpatterns = [   
    url(r'^$', views.index, name='index'),
]

###########################################
# from django.urls import path

# from . import views

# urlpatterns = [    
#     path('', views.hello, name='hello'),
# ]
