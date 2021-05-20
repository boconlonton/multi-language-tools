from django.urls import path

from . import views

urlpatterns = [
    path('', views.screen_home, name='screen-home'),
    path('create', views.screen_create, name='screen-create'),
    path('<int:screen_id>', views.screen_detail, name='screen-detail')
]
