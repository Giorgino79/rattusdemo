from django.urls import path
from .views import   (vediservizio, elencoservizi, nuovoservizio, 
                      DistintaInserisci,elencodistinte,chiudirecuperoview,
                      servizioprivati, cancelladist,aggiornadistinta,aggservizioazienda,aggservizioprivati,
                      pdfconferma,   chiudiserv,chiudidist, 
                      vedidistinta2,  elencodistintechiuse,nuovoservizioaziende, 
                      elencoservizipdf,sceglicliente, pdf_view, chiudiincassidistinta,chiudiserv2)
app_name='servizi'

urlpatterns = [

    path('sceltacliente', nuovoservizio, name='nuovo-servizio'),
    path('sceglicodicecliente', sceglicliente, name='sceglicliente'),
    path('servizioaziende/<pk>', nuovoservizioaziende, name='servizioaziende' ),
    path('aggservizioazienda/<pk>', aggservizioazienda, name='aggservizioazienda' ),
    path('aggservizioprivati/<pk>', aggservizioprivati, name='aggservizioprivati' ),
    path('servizioprivati', servizioprivati, name='servizioprivati' ),
    path('elencoservizi/', elencoservizi, name='elencoservizi'),
    path('elencoservizi/<int:pk>', vediservizio, name='vediservizio'),
    path('pdf/<pk>',pdfconferma,name='pdf'),
    path('nuovadistinta', DistintaInserisci.as_view(), name='distinta'),
    path('elencodistinte', elencodistinte, name='elencodistinte'),
    path('aggiornadistinta/<pk>', aggiornadistinta, name='aggiornadistinta'),
    path('elencodistintechiuse', elencodistintechiuse, name='elencodistintechiuse'),
    path('elencodistinte/<int:pk>', vedidistinta2,name='vedidistinta'),
    path('chiudidistinta/<int:pk>', chiudiincassidistinta,name='chiudidistinta'),
    path('chiudiservizio/<int:pk>', chiudiserv2,name='chiudiservizio'),
    path('cancelladistinta/<int:pk>',cancelladist, name='cancella'),
    path('chiudirecupero/<pk>',chiudirecuperoview,name='chiudirecupero'),
    path('servizidelmese/',elencoservizipdf,name='elencoservizipdf'),
    path('vedipdf/<int:pk>', pdf_view,name='vedipdf'),

]
 