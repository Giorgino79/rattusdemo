from django.db import models
from anagrafica.models import Azienda, Privati, Filiali
from contratti.models import Contratto
from automezzi.models import Automezzo, ManutenzioneMezzi
from django.urls import reverse
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.core.files.base import ContentFile
from io import BytesIO
from django.core.files import File
from django.contrib.auth.models import User
from logistica.models import Products,Warehouse
    


SERVIZIO=['Disinfestazione','Derattizzazione', 'Deformicazione', 'Deblattizzazione', 'Rimozione Guano', 'Raccolta Carcasse', 'Cambio Postazioni Mosche', 'Altro', 'Giardinaggio','Antitarlo']
SCEGLISERVIZIO=sorted([(item, item)for item in SERVIZIO])



     
    

class Servizio(models.Model):

    azienda=models.ForeignKey(Azienda, on_delete=models.CASCADE, null=True, blank=True)
    contratto=models.ForeignKey(Contratto, on_delete=models.CASCADE, null=True, blank=True, related_name='contratto')
    privati=models.ForeignKey(Privati, on_delete=models.CASCADE, null=True, blank=True)
    filiali=models.ForeignKey(Filiali, on_delete=models.CASCADE, null=True, blank=True)
    data_espletazione=models.DateField(null=True, blank=True)
    altro_luogo=models.CharField(max_length=200, null=True, blank=True)
    luogo_effettivo=models.CharField(max_length=200, null=True, blank=True)
    prezzo=models.FloatField(null=True, blank=True)
    inespl=models.BooleanField(default=False)
    incasso=models.BooleanField(default=False)
    importo_incassato=models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    Tiposervizio=models.CharField(max_length=200, choices=SCEGLISERVIZIO, blank=True, null=True)
    prodotto=models.ForeignKey(Products, on_delete=models.CASCADE, null=True, blank=True)
    note=models.CharField(max_length=244, null=True, blank=True)
    espletato=models.BooleanField(default=False)
    orario_inizio=models.TimeField(blank=True, null=True)
    pdf=models.FileField(upload_to='media/servizi', blank=True, null=True)
    data_chiusura=models.DateField(auto_now=False, blank=True, null=True)
    
        
    @property
    def servizio(self):
        return self.servizio_set.all()
    
    def get_queryset(self):
        return Servizio.object.all()
    
    def get_absolute_url(self):
        return reverse("servizi:vediservizio", kwargs={"pk": self.pk})
    
    def salva(self, **kwargs):
        if not self.prezzo:
            self.prezzo=self.contratto.pk
        if self.azienda:
            self.luogo_effettivo=self.azienda.indSedeLegale
        elif self.filiali:
            self.luogo_effettivo=self.filiali.indFiliale
        else:
            self.luogo_effettivo=self.altro_luogo
        
        
        
        super().save(**kwargs)

    
    def __str__(self):
        cliente=''
        if self.azienda:
            cliente=self.azienda
        else:
            cliente= self.privati
        indirizzo=''
        return f'{self.pk} - {self.Tiposervizio} - {cliente} - {indirizzo}'

  
        
class Recupero(models.Model):
    servizio=models.ForeignKey(Servizio, on_delete=models.CASCADE, related_query_name='serv')
    data_creazione=models.DateField(auto_now_add=True, blank=True,null=True)
    importo_da_recuperare=models.FloatField(blank=True, null=True)
    data=models.DateField(blank=True, null=True)
    note=models.TextField(max_length=2000,blank=True, null=True)
    chiuso=models.BooleanField(default=False)
    data_chiusura=models.DateField(blank=True,null=True)
    
    def get_absolute_url(self):
        return reverse("contabilità:vedirecupero", kwargs={"pk": self.pk})
    
    def __str__(self):
        return f'{self.servizio}, importo da recuperare: {self.importo_da_recuperare}'    
  


class Distinte(models.Model):
    user=models.ForeignKey('dipendenti.Dipendente', on_delete=models.CASCADE,blank=True, null=True)
    servizio=models.ManyToManyField(Servizio, related_name='servizio', related_query_name='ser')
    recupero=models.ManyToManyField(Recupero, related_query_name='recupero', blank=True )
    servizio_di_manutenzione=models.ForeignKey(ManutenzioneMezzi, on_delete=models.CASCADE,blank=True, null=True)
    automezzo=models.ForeignKey(Automezzo, on_delete=models.CASCADE,blank=True, null=True)
    data=models.DateField(blank=True, null=True)
    chiusura=models.BooleanField(default=False)
    
    def get_absolute_url(self):
        return reverse("servizi:vedidistinta", kwargs={"pk": self.pk})
    
    
    def __str__(self):
        return f'{self.pk} - {self.user} - {self.data}  - {self.automezzo}'
  