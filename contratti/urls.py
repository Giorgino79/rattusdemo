from django.urls import path
from .views import nuovocontratto, elencocontratti,modificacontratto,vedicontratti,eliminacontratto

app_name='contratti'


urlpatterns = [
    path('nuovocontratto', nuovocontratto, name='nuovocontratto'),
    path('elencocontratti', elencocontratti, name='elencocontratti'),
    path('modificacontratto/<int:pk>', modificacontratto, name='modificacontratto'),
    path('vedicontratti/<int:pk>', vedicontratti, name='vedicontratti'),
    path('eliminacontratto/<int:pk>', eliminacontratto, name='eliminacontratto'),
    
    
]
