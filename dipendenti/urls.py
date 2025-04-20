from django.urls import path
from .views import (registradipendente, esci,vedidipendente,
                    elencodipendenti, entra, aggiornadipendente, 
                    profilo, giornatemesedipendente, nuovagiornata,aggiornagiornata)
app_name='dipendenti'

urlpatterns = [
    path('',entra,name='login'),
    path('logout',esci,name='logout'),
    path('nuovodipendente',registradipendente,name='nuovodip'),
    path('dipendenti', elencodipendenti,name='elencodipendenti'),
    path('aggiornadipendente/<int:pk>', aggiornadipendente,name='aggiornadipendente'),
    path('vedidipendente/<int:pk>', vedidipendente,name='vedidipendente'),
    path('profilo/<str:username>',profilo, name='profilo'),
    path('inziogiorno',nuovagiornata,name='nuovagiornata'),
    path('aggiornagiornata/<int:pk>',aggiornagiornata,name='aggiornagiornata'),
    path('giornatemesedipendente',giornatemesedipendente,name='giornatemesedipendente'),
    
    
]
