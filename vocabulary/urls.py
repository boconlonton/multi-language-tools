from django.urls import path

from . import views

urlpatterns = [
    path('', views.vocab_home, name='vocab-home'),
    path('create', views.vocab_create, name='vocab-create'),
    path('<int:vocab_id>', views.vocab_detail, name='vocab-detail'),
    path('<int:vocab_id>/<int:screen_id>', views.vocab_delete_screen, name='vocab-delete-screen')
]
