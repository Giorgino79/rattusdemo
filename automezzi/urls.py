from django.urls import path
from .views import (nuovomezzo, elencomezzi, aggiornamezzo,vedimezzo, 
                    NuovoIntervento, elencointerventi, vediintervento, vediprodottimezzo,
                    rifornimento, nuovacartacarburante, vedicartacarburante)
app_name='automezzi'

urlpatterns = [
    path('nuovo-mezzo',nuovomezzo, name='nuovo-mezzo'),
    path('elenco-mezzi', elencomezzi, name='elenco-mezzi'),
    path('elenco-mezzi/<int:pk>', vedimezzo, name='scheda-mezzo'),
    path('nuovo-intervento', NuovoIntervento.as_view(), name='nuovo-intervento'),
    path('elenco-interventi', elencointerventi, name='elenco-interventi'),
    path('elenco-interventi/<int:pk>', vediintervento, name='scheda-intervento'),
    path('vediprodottimezzo/<pk>', vediprodottimezzo, name='giacenzamezzo'),
    path('aggiornaschedamezzo/<int:pk>',aggiornamezzo,name='aggiornamezzo'),
    
    path('rifornimento',rifornimento,name='rifornimento'),
    path('nuovacartacarburante',nuovacartacarburante,name='nuovacartacarburante'),
    path('elencorifornimenti',vedicartacarburante,name='vedicartacarburante')


]
