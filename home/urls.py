from django.urls import path
from . import views
app_name='home'

urlpatterns = [
    path('home/', views.home,name='home'),
    path('cerca', views.cerca,name='funzione-cerca'),
    path('chat', views.chat, name='chat'),
    path('eliminamessaggio/<int:pk>',views.DeleteMessage.as_view(),name='elimina')
]
