from django.db import models
from servizi.models import Servizio
from django.shortcuts import reverse
from anagrafica.models import Azienda,Fornitori,Privati
from logistica.models import Order
from datetime import datetime
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

class Versamenti(models.Model):
    causale=models.CharField(max_length=200)
    data=models.DateField()
    dare=models.FloatField()
    avere=models.FloatField()
    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id=models.PositiveIntegerField()
    content_object=GenericForeignKey('content_type','object_id')
    
    def str(self):
        return self.data, self.casuale, self.dare, self.avere
    
    class Meta:
        indexes=[models.Index(fields=['content_type', 'object_id'])]



class Banca(models.Model):
    nome=models.CharField(max_length=200)
    iban=models.CharField(max_length=27)
    indirizzo=models.CharField(max_length=200, null=True, blank=True)
    cap=models.CharField(max_length=5, null=True,blank=True)
    città=models.CharField(max_length=200, null=True,blank=True)
    
    def get_absolute_url(self):
        return reverse("contabilità:vedibanca", kwargs={"pk": self.pk})
    
    def __str__(self):
        return f'{self.nome}'
    
    

class NumeroCassa(models.Model):
    nome=models.CharField(max_length=200)
    
    def __str__(self):
        return f'{self.nome}'


ALIQUOTE=[4.00,5.00,10.00,22.00]
SCEGLIALIQUOTA=sorted([(item, item)for item in ALIQUOTE])

class FatturaAttiva(models.Model):
    
    data_fattura=models.DateField(auto_now=False, default=datetime.now )
    azienda=models.ForeignKey(Azienda, on_delete=models.CASCADE, blank=True,null=True)
    privato=models.ForeignKey(Privati,on_delete=models.CASCADE, blank=True,null=True)
    fornitori=models.ForeignKey(Fornitori, on_delete=models.CASCADE, blank=True,null=True)
    imponibile=models.FloatField()
    importoiva=models.FloatField(default=0)
    totale=models.FloatField(default=0, blank=True, null=True)
    descrizione=models.TextField(max_length=4000)
    da_incassare=models.BooleanField(default=True)
    data_scadenza=models.DateField(blank=True,null=True)
    data_pagamento=models.DateField(blank=True,null=True)
    avere=models.FloatField(null=True,blank=True)
    dare=models.FloatField(null=True,blank=True)
    pdf=models.FileField(upload_to='contabilità/fattureattive/', blank=True, null=True)
    
    def __str__(self):
        return f'{self.pk} - {self.azienda.ragioneSociale} - {self.fornitori.ragioneSociale} - {self.privato.nome_cognome} - {self.totale} €'
    

class FatturaPassiva(models.Model):
    data_fattura=models.DateField()
    numero_fattura=models.CharField(max_length=50, default='')
    fornitori=models.ForeignKey(Fornitori, on_delete=models.CASCADE, blank=True,null=True)
    ordini_acquisto=models.ManyToManyField(Order)
    imponibile=models.FloatField()
    iva=models.FloatField( choices=SCEGLIALIQUOTA, default=22.00)
    descrizione=models.TextField(max_length=10000)
    da_pagare=models.BooleanField(default=True)
    data_pagamento=models.DateField(blank=True,null=True)
    totale=models.FloatField(default=0)
    avere=models.FloatField(null=True,blank=True)
    dare=models.FloatField(null=True,blank=True)

    pdf=models.FileField(upload_to='media/contabilità/fatturepassive', blank=True, null=True)
    
    def __str__(self):
        return f'{self.pk} - {self.fornitori.ragioneSociale} - {self.totale} €'


class Movimenti(models.Model):
    fattura_passiva=models.ForeignKey(FatturaPassiva, on_delete=models.CASCADE, null=True,blank=True)
    fattura_attiva=models.ForeignKey(FatturaAttiva, on_delete=models.CASCADE, null=True,blank=True)
    banca=models.ForeignKey(Banca, on_delete=models.CASCADE, null=True,blank=True, related_name='banca')
    cassa=models.ForeignKey(NumeroCassa, on_delete=models.CASCADE, blank=True, null=True, related_name='cassa')
    data=models.DateField()
    causale=models.CharField(max_length=1000)
    importo=models.FloatField(blank=True,null=True)
    aggiungifile=models.FileField(upload_to='media/contabilità', null=True,blank=True)

    
    def __str__(self):
        return f'{self.pk}'



class Cassa(models.Model):
    numero_cassa=models.ForeignKey(NumeroCassa,on_delete=models.CASCADE, related_name='cax' ,blank=True,null=True)
    causale=models.CharField(max_length=1500, blank=True, null=True)
    servizio=models.ForeignKey(Servizio, on_delete=models.CASCADE, default=None, blank=True, null=True)
    data=models.DateField( blank=True, null=True)
    cassaavere=models.FloatField(blank=True, null=True, default=0)
    cassadare=models.FloatField(blank=True, null=True, default=0)
    aggiungifile=models.FileField(upload_to='media/contabilità', null=True,blank=True)
    versamenti=GenericRelation(Versamenti)
    fattureattiva=models.ForeignKey(FatturaAttiva,blank=True,null=True, on_delete=models.CASCADE)
    fatturapassiva=models.ForeignKey(FatturaPassiva,blank=True,null=True, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.numero_cassa.nome} - Avere: {self.cassaavere} - Dare: {self.cassadare}'    


class BancaMovimenti(models.Model):
    banca=models.ForeignKey(Banca, on_delete=models.CASCADE, blank=True, null=True)
    causale=models.CharField(max_length=1500, blank=True, null=True)
    data=models.DateField(blank=True, null=True)
    avere=models.FloatField(null=True,blank=True)
    dare=models.FloatField(null=True,blank=True)
    versamenti=GenericRelation(Versamenti)
    aggiungifile=models.FileField(upload_to='media/contabilità', null=True,blank=True)
    fattureattiva=models.ForeignKey(FatturaAttiva,blank=True,null=True, on_delete=models.CASCADE)
    fatturapassiva=models.ForeignKey(FatturaPassiva,blank=True,null=True, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.banca}'