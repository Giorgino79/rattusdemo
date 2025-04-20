
from django.db import models
from django.urls import reverse
from anagrafica.models import Fornitori
from logistica.models import Products, Warehouse
from datetime import timedelta,datetime
from django.utils import timezone


TIPO=['Gasolio', 'Benzina', 'Metano', 'Elettrica']
TIPOALIMENTAZIONE=sorted([(item, item)for item in TIPO])



class Automezzo(models.Model):
    targa=models.CharField(max_length=7)
    marca=models.CharField(max_length=200)
    modello=models.CharField(max_length=200)
    foto=models.ImageField(upload_to='media/media', blank=True, null=True)    
    data_revisione=models.DateField()
    alimentazione=models.CharField(max_length=50, choices=TIPOALIMENTAZIONE)
    data_acquisto=models.DateField()
    valore_acquisto=models.DecimalField(max_digits=10, decimal_places=2)
    note=models.TextField(blank=True, null=True)
    data_alienazione=models.DateField(blank=True, null=True)
    alienato=models.BooleanField(default=False)
    
    def get_absolute_url(self):
        return reverse("automezzi:scheda-mezzo", kwargs={"pk": self.pk})
    
    @property
    def mezzo(self):
        return self.mezzo_set.all()
    
    def __str__(self):
        return f'{self.targa}'
    
TIPO=['Cambio Olio','Cambio Gomme', 'Cambio Filtri', 'Revisione', 'Carrozzeria', 'Lavaggio', 'Allestimento', 'Elettrauto']
TIPOINTERVENTO=sorted([(item, item)for item in TIPO])

class ManutenzioneMezzi(models.Model):
    mezzo=models.ForeignKey(Automezzo, on_delete=models.CASCADE)   
    fornitore=models.ForeignKey(Fornitori, on_delete=models.CASCADE, blank=True, null=True) 
    data_intervento=models.DateField(null=True, blank=True)
    intervento=models.CharField(max_length=50, choices=TIPOINTERVENTO, null=True, blank=True)
    costo_intervento=models.DecimalField(max_digits=10, decimal_places=2)
    note=models.TextField(max_length=400, null=True, blank=True)
    ora=models.TimeField(null=True,blank=True)
    
    def __str__(self):
        return f'{self.data_intervento} - {self.mezzo}'
    
    @property
    def manutenzione(self):
        return self.manutenzione_set.all()
    
    def get_absolute_url(self):
        return reverse("automezzi:scheda-intervento", kwargs={"pk": self.pk}) 

class MagazzinoMezzo(models.Model):
    mezzo=models.ForeignKey(Automezzo,on_delete=models.CASCADE)
    prodotto=models.ForeignKey(Products, on_delete=models.CASCADE, null=True,blank=True)
    data_entrata=models.DateField(auto_now_add=False, null=True,blank=True)
    data_uscita=models.DateField(auto_now_add=False, null=True,blank=True)
    giacenza=models.PositiveIntegerField(default=0,null=True,blank=True)
    
    def __str__(self):
        return f'{self.mezzo}'





class CartaCarburante(models.Model):
    nome =models.CharField(max_length=50)
    fornitore=models.ForeignKey(Fornitori, on_delete=models.CASCADE)
    limite=models.FloatField()
    residuo=models.FloatField(null=True,blank=True)
    def __str__(self):
        return f'{self.nome} - {self.fornitore}'
    

  

class Rifornimento(models.Model):
    operatore=models.ForeignKey('dipendenti.Dipendente',on_delete=models.CASCADE, null=True, blank=True)
    mezzo=models.ForeignKey(Automezzo,on_delete=models.CASCADE, null=True, blank=True)
    carta=models.ForeignKey(CartaCarburante, on_delete=models.CASCADE)
    data=models.DateField(auto_now=True)
    importo=models.FloatField()
    residuo=models.FloatField(blank=True, null=True)
    
    
    def __str__(self):
        return f'{self.operatore} - {self.data} - {self.mezzo} - {self.importo}'
    