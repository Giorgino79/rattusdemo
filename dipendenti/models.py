from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.urls import reverse
from django.contrib.auth import get_user_model
import datetime
from automezzi.models import Automezzo



class Dipendente(AbstractUser):
    class Autorizzazioni(models.TextChoices):
        totale='totale', 'Tutte le autorizzazioni',
        contabile='contabile', 'anagrafica, contabilità, automezzi, servizi'
        operativo='operativo', 'automezzi, servizi, magazzino'
        operatore='operatore','servizi, magazzino(mezzo affidato)'
    livello=models.CharField(max_length=30, choices=Autorizzazioni.choices, default='operatore')
    indirizzo=models.CharField(max_length=500, blank=True, null=True)
    CF=models.CharField(verbose_name='Codice Fiscale',max_length=16, blank=True, null=True)
    carta_d_identità=models.CharField(verbose_name="Numero della carta di identità",max_length=200, blank=True, null=True)
    patente_di_guida=models.CharField(verbose_name="Numero della patente di guida",max_length=200, blank=True, null=True)
    foto_dipendente=models.ImageField(upload_to='media/dipendenti', blank=True, null=True)
    posizione_inail=models.CharField(max_length=200, blank=True, null=True)
    posizione_inps=models.CharField(max_length=200, blank=True, null=True)
    foto_carta_identità=models.ImageField(upload_to='media/dipendenti', blank=True, null=True)
    foto_codice_fiscale=models.ImageField(upload_to='media/dipendenti', blank=True, null=True)
    foto_patente=models.ImageField(upload_to='media/dipendenti', blank=True, null=True)
    all1=models.FileField(verbose_name='allegato visibile al dipendente',upload_to='media/dipendenti', blank=True, null=True)
    all2=models.FileField(verbose_name='allegato visibile al dipendente',upload_to='media/dipendenti', blank=True, null=True)
    all3=models.FileField(verbose_name='allegato non visibile al dipendente',upload_to='media/dipendenti', blank=True, null=True)
    all4=models.FileField(verbose_name='allegato non visibile al dipendente',upload_to='media/dipendenti', blank=True, null=True)
    note=models.TextField(max_length=4000,blank=True,null=True)
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="dipendente_set",
        related_query_name="dipendente",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="dipendente_set",
        related_query_name="dipendente",
    )

    
    def get_absolute_url(self):
        return reverse("dipendenti:vedidipendente", kwargs={"pk": self.pk})
    
    def __str__(self):
        return f'{self.username}'


class Giornata(models.Model):
    dip=get_user_model()
    data=models.DateField(auto_now_add=True)
    operatore=models.ForeignKey(dip,on_delete=models.CASCADE)
    mezzo=models.ForeignKey(Automezzo,on_delete=models.CASCADE)
    ora_inizio_mattina=models.TimeField(blank=True,null=True)
    ora_fine_mattina=models.TimeField(blank=True,null=True)
    ora_inizio_pomeriggio=models.TimeField(blank=True,null=True)
    ora_fine_pomeriggio=models.TimeField(blank=True,null=True)
    chiudi_giornata=models.BooleanField(default=False)
    
    class Meta:
        unique_together=('operatore','data')
    def __str__(self):
        return f'{self.data} - {self.operatore}'
    
    def daily_hours(self):
        total = datetime.timedelta()
        
        print(f"\n--- Calcolo ore per {self.data} ---")
        print(f"Mattina: {self.ora_inizio_mattina} → {self.ora_fine_mattina}")
        print(f"Pomeriggio: {self.ora_inizio_pomeriggio} → {self.ora_fine_pomeriggio}")
        try:
            if self.ora_inizio_mattina and self.ora_fine_mattina:
                mattina = datetime.combine(self.data, self.ora_fine_mattina) - datetime.combine(self.data, self.ora_inizio_mattina)
                total += mattina
        except:
            pass  # 
        try:
            if self.ora_inizio_pomeriggio and self.ora_fine_pomeriggio:
                pomeriggio = datetime.combine(self.data,self.ora_fine_pomeriggio) - datetime.combine(self.data, self.ora_inizio_pomeriggio)
                total += pomeriggio
        except:
            pass  # 
        print(f"Totale calcolato: {total}")
        
        if (
            self.ora_inizio_mattina and self.ora_fine_pomeriggio
            and not self.ora_fine_mattina
            and not self.ora_inizio_pomeriggio
            ):
            try:
                total += datetime.combine(self.data, self.ora_fine_pomeriggio) - datetime.combine(self.data, self.ora_inizio_mattina)
            except Exception as e:
                pass

        return total
     