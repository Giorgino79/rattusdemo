from django.db import models

# Create your models here.
from django.db import models
from anagrafica.models import Fornitori
from django.urls import reverse, reverse_lazy
import django.utils.timezone as time 
from django.core.validators import MaxValueValidator, MinValueValidator
from anagrafica.models import Privati,Azienda,Fornitori, Filiali
from django.utils import timezone
import datetime
from django.core.exceptions import ValidationError

MISURA=['Litro', 'Articolo', 'Millilitri per Articolo', 'Grammi per Articolo']
TIPOMISURA=sorted([(item, item)for item in MISURA])
STATO=['Liquido', 'Polvere', 'Singolo Prodotto', 'Gel']
TIPOSTATO=sorted([(item, item)for item in STATO])

class Products(models.Model):
    fornitore=models.ForeignKey(Fornitori, on_delete=models.CASCADE)
    nome_prodotto=models.CharField(max_length=200)
    Registro_ministero_della_salute=models.TextField()
    note=models.TextField()
    tipo_articolo=models.CharField(max_length=50, choices=TIPOSTATO)
    misura=models.CharField(max_length=50, choices=TIPOMISURA)
    prezzo=models.FloatField(default=0, null=True, blank=True)
    
    
    def get_absolute_url(self):
        return reverse("logistica:vediprodotto", kwargs={"pk": self.pk})
    
    def __str__(self):
        return f'{self.nome_prodotto}'
    

class Order(models.Model):
    prodotto=models.ForeignKey(Products, on_delete=models.CASCADE)
    fornitore=models.ForeignKey(Fornitori,on_delete=models.CASCADE,null=True, blank=True)
    numero_articoli=models.FloatField()
    prezzo_singolo_articolo=models.FloatField()
    data_ordine=models.DateField(auto_now_add=True)
    data_arrivo_ordine=models.DateField(auto_now_add=False)
    indirizzo_consegna=models.CharField(max_length=300)
    pagamento=models.CharField(blank=True, null=True, max_length=200) 
    note=models.TextField(blank=True, null=True)
    ricevuto=models.BooleanField(default=False)
    data_ricezione=models.DateField(auto_now_add=False, null=True,blank=True)
    importo_ordine=models.FloatField(blank=True, null=True)
    articoli_ricevuti=models.FloatField(blank=True, null=True)
    pdf=models.FileField(upload_to='media/ordini-acquisto', blank=True, null=True)
    pagato=models.BooleanField(default=False,blank=True,null=True)
    def get_absolute_url(self):
        return reverse("logistica:vediordine", kwargs={"pk": self.pk})
    def __str__(self):
        return f'{self.pk} - {self.prodotto} - {self.prodotto.fornitore}'

class Warehouse(models.Model):
    prodotto=models.ForeignKey(Products, on_delete=models.CASCADE, null=True,blank=True)
    ordine=models.ForeignKey(Order, on_delete=models.CASCADE, null=True,blank=True)
    data_entrata=models.DateField(auto_now_add=False, null=True,blank=True)
    data_uscita=models.DateField(auto_now_add=False, null=True,blank=True)
    giacenza=models.FloatField(blank=True, null=True)
    bolla_ingresso_merci=models.ImageField(upload_to='media/documenti_merci_in_entrata', blank=True, null=True)
    soglia_giacenza=models.FloatField(default=10)
    
    def clean(self):
        super().clean()
        if self.giacenza < 0:
            raise ValidationError({'giacenza': 'La giacenza non può essere negativa.'})
        if self.soglia_giacenza < 0:
            raise ValidationError({'soglia_allerta': 'La soglia di allerta non può essere negativa.'})
        if self.soglia_giacenza > self.giacenza:
            raise ValidationError({'soglia_allerta': 'La soglia di allerta non può essere superiore alla giacenza attuale.'})

    def __str__(self):
        return f'{self.prodotto.nome_prodotto}'
    


from django.utils.timezone import now
class Install(models.Model):
        azienda=models.ForeignKey(Azienda,on_delete=models.CASCADE, blank=True, null=True, related_name='azienda')
        privato=models.ForeignKey(Privati,on_delete=models.CASCADE, blank=True, null=True)
        filiale=models.ForeignKey(Filiali,on_delete=models.CASCADE, blank=True, null=True)
        data_installazione=models.DateField(default=now())
        prodotto=models.ForeignKey(Products, on_delete=models.CASCADE, blank=True, null=True)
        quantità=models.PositiveIntegerField(blank=True, null=True)
        cartelli=models.IntegerField(blank=True, null=True)
        totale_postazioni=models.IntegerField(default=0)
        note=models.TextField(null=True, blank=True)
        pdf=models.FileField(upload_to='media/installazioni', null=True,blank=True)
        def __str__(self):
            return f'{self.azienda} {self.privato} {self.filiale}'