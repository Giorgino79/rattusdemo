from django.urls import path
from .views import (incassi, crearecupero, vedirecuperi, 
                    chiudiincasso,vedicassa, aggiornarecupero,
                    Bancanuova, elencobanche, AggiornaAnagraficaBanca, 
                     FatturaPassivaView, 
                    elencofattureattive,elencofatturepassive,vedimovimentibanca,
                    movimenti, mese,CassaNuova, vedimovimentibanca,invio_fattura_pdf,
                    fatturazione,vedirecupero,prelievo,versamento, vedipdf)

app_name='contabilità'

urlpatterns = [
    path('incassi-inevasi', incassi,name='inevaso'),
    path('nuovorecupero/<int:pk>',crearecupero,name='recupero'),
    path('vedirecupero',vedirecuperi,name='elencorecupero'),
    path('chiudiincasso/<int:pk>',chiudiincasso,name='chiudiincasso'),
    path('cassa',vedicassa,name='cassa'),
    path('aggiornarecupero/<int:pk>',aggiornarecupero,name='aggiornarecupero'),
    path('nuovabanca/', Bancanuova.as_view(),name='nuovabanca'),
    path('elencobanche', elencobanche, name='elencobanche'),
    path('vedibanca/<pk>', vedimovimentibanca, name='vedibanca'),
    path('movimenti', movimenti, name='movimenti'),
    path('aggiornaanagraficabanca', AggiornaAnagraficaBanca.as_view(), name='aggiornaanagraficabanca'),
    path('nuovafattura',fatturazione,name='nuovafattura'),
    path('registrafattura',FatturaPassivaView.as_view(),name='registrafattura'),
    path('elencofattureattive',elencofattureattive,name='elencofattureattive'),
    path('elencofatturepassive',elencofatturepassive,name='elencofatturepassive'),
    path('scegliservizi',mese,name='scegliservizi'),
    path('nuovacassa',CassaNuova.as_view(),name='nuovacassa'),
    path('pdffattura/<pk>', invio_fattura_pdf, name='pdffattura'), 
    path('vedirecupero/<pk>', vedirecupero, name='vedirecupero'),
    path('prelievo', prelievo, name='prelievo'),
    path('versamento', versamento, name='versamento'),
    path('vedifattura/<pk>', vedipdf, name='vedipdf' )

    ]