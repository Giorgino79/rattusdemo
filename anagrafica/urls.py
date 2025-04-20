from django.urls import path
from .views import (InsAna, InsFil, vediana, elenco, aggazienda,aggprivato,aggfornitore, 
                    InsFor, elencofornitori, vedifor, Inspriv, elencoprivati, vedipriv,
                    aggiornafiliale, elencofiliali)

app_name='anagrafica'

urlpatterns = [
    path('nuova-anagrafica/', InsAna.as_view(), name='nuova-anagrafica'),
    path('aggiornaanagrafica/<int:pk>', aggazienda, name='aggiornaazienda'),
    path('filiali', InsFil.as_view(), name='filiali'),
    path('elencoclienti/', elenco, name='elencoclienti'),
    path('elencoclienti/<int:pk>/', vediana, name='vedicodice'),
    path('nuovo-fornitore/', InsFor.as_view(), name='nuovo-fornitore'),
    path('aggiorna-fornitore/<pk>', aggfornitore, name='aggiornafornitore'),
    path('elencofornitori/', elencofornitori, name='elencofornitori'),
    path('elencofornitori/<int:pk>', vedifor, name='vedifornitore'),
    path('nuovo-privato', Inspriv.as_view(), name='nuovo-privato' ),
    path('nuovo-privato/<int:pk>', aggprivato, name='aggiornaprivato' ),
    path('elencoprivati', elencoprivati, name='elencoprivati' ),
    path('elencoprivati/<int:pk>', vedipriv, name='vediprivato' ),
    path('elencofiliali',elencofiliali,name='elencofiliali'),
    path('aggiornafiliale/<int:pk>',aggiornafiliale,name='aggiornafiliale')
    
    
]
