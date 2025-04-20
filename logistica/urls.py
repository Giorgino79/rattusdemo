from django.urls import  path
from .views import (prodotto, elencoprodotti,Aggiornaprodotto, 
                    elencoordininonricevuti, elencoordiniricevuti, ordiniprodotto, 
                    magazzino, ricezioneordine, vediordine, inviaordinepdf,
                    nuovoordine, Vediprodotto, ScegliMezzo,
                    installazione,reportinstallazione,invioreportinstallazione,elencoinstallazioni,aggiornainstallazione,
                    ordine_pdf, carica_mezzo, vedimezzocarico, vecchiainstallazione)

app_name='logistica'

urlpatterns = [
    path('nuovo-prodotto',prodotto,name='nuovo-prodotto'),
    path('elencoprodotti',elencoprodotti,name='elencoprodotti'),
    path('aggiornaprodotto/<pk>',Aggiornaprodotto,name='aggiornaprodotto'),
    path('vediprodotto/<pk>',Vediprodotto,name='vediprodotto'),
    
    path('ordinidaricevere',elencoordininonricevuti,name='ordinidaricevere'),    
    path('ordiniricevuti',elencoordiniricevuti,name='ordiniricevuti'),    
    path('nuovo-ordine',nuovoordine,name='nuovo-ordine'),
    path('vediordine/<pk>',vediordine,name='vediordine'),
    path('ordineprodotto/<pk>',ordiniprodotto,name='ordineprodotto'),
    path('ricezioneordini/<int:pk>/', ricezioneordine, name='ricezione'),
    path('inviapdfordine/<int:pk>/', inviaordinepdf,name='invioordinepdf'),
    path('pdf-ordine/<pk>', ordine_pdf, name='pdf-ordine'),

    path('magazzino', magazzino, name='magazzino'),
    path('sceglimezzo', ScegliMezzo,name='sceglimezzo'),
    path('caricamezzo/<pk>', carica_mezzo, name='caricamezzo'),    
    path('vedicarico/<pk>', vedimezzocarico, name='mezzocarico'),    
    
    path('installazione',installazione, name='installazione'),
    path('vecchiainstallazione',vecchiainstallazione, name='vecchiainstallazione'),
    path('report-installazione/<pk>',reportinstallazione, name='reportinstallazione'),
    path('invio-report-installazione/<pk>',invioreportinstallazione, name='invioreportinstallazione'),
    path('elencoinstallazioni',elencoinstallazioni, name='elencoinstallazioni'),
    path('elencoinstallazioni/<pk>',aggiornainstallazione, name='agginstall'),
    
    path('caricamezzo/<int:pk>',carica_mezzo,name='caricamezzo')
    
]
