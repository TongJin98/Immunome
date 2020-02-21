from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload', views.upload_file, name='upload'),
    path('success', views.success, name='success'),
    #path('test1',views.test1, name='test1'),
]
