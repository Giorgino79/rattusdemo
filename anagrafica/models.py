from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse

TIPO=['Azienda unica', 'Multifiliale', 'Condominio']
TIPOAZIENDA=sorted([(item, item)for item in TIPO])
PAGAMENTO=['Immediato', '30gg', '60gg', '90gg']
TIPOPAG=sorted([(item,item)for item in PAGAMENTO])

class Azienda(models.Model):
    class Pagatipo(models.TextChoices):
        IMMEDIATO='01', 'Immediato',
        TRENTA='30', '30 gg df'
        SESSANTA='60', '60 gg df'
        NOVANTA='90','90 gg df'    
    ragioneSociale=models.CharField(max_length=200)
    indSedeLegale=models.CharField(max_length=200)
    cittaLegale=models.CharField(max_length=200)
    provincia=models.CharField(max_length=2)
    capLegale=models.IntegerField()
    PI=models.CharField(max_length=11)
    CF=models.CharField(max_length=16)
    CU=models.CharField(max_length=7)
    tipo=models.CharField(max_length=15, choices=TIPOAZIENDA, default='Azienda unica')
    referente=models.CharField(max_length=200)
    telefono=models.CharField(max_length=20)
    pec=models.EmailField()
    mailDirezione=models.EmailField(blank=True, null=True)
    mailAmministrazione=models.EmailField(blank=True, null=True)
    mailOperativo1=models.EmailField()
    mailOperativo2=models.EmailField(blank=True, null=True)
    mailOperativo3=models.EmailField(blank=True, null=True)
    modpag=models.CharField(max_length=20, choices=Pagatipo.choices, default='Immediato')
    installato=models.BooleanField(default=False, blank=True,null=True)
    
    @property
    def azienda(self):
        return self.azienda_set.all()
    
    def get_absolute_url(self):
        return reverse("anagrafica:vedicodice", kwargs={"pk": self.pk})
    
    def __str__(self):
        return f'{self.ragioneSociale}'
    
    

class Filiali(models.Model):
    
    anaFiliale=models.ForeignKey(Azienda, on_delete=models.CASCADE)
    nomeFiliale=models.CharField(max_length=200)
    indFiliale=models.CharField(max_length=200)
    cittaFiliale=models.CharField(max_length=200)
    capFiliale=models.CharField(max_length=5)
    telFiliale=models.CharField(max_length=200)
    mailFiliale=models.CharField(max_length=200)
    referenteFiliale=models.CharField(max_length=50, blank=True, null=True)
    installato=models.BooleanField(default=False, blank=True,null=True)

    @property
    def filiale(self):
        return self.filiale_set.all()
    
    def get_absolute_url(self):
        return reverse("azienda:vedicodice", kwargs={"pk": self.pk})
     
    def __str__(self):
        return f'{self.nomeFiliale} - indirizzo: {self.indFiliale}'
    

class Fornitori(models.Model):
    ragioneSociale=models.CharField(max_length=200)
    indSedeLegale=models.CharField(max_length=200)
    cittaLegale=models.CharField(max_length=200)
    provincia=models.CharField(max_length=2)
    capLegale=models.IntegerField()
    PI=models.IntegerField()
    CF=models.CharField(max_length=16)
    CU=models.CharField(max_length=7)
    referente=models.CharField(max_length=200)
    telefono=models.CharField(max_length=20)
    pec=models.EmailField()
    mailDirezione=models.EmailField(blank=True, null=True)
    mailAmministrazione=models.EmailField(blank=True, null=True)
    mailOperativo1=models.EmailField()
    mailOperativo2=models.EmailField(blank=True, null=True)
    mailOperativo3=models.EmailField(blank=True, null=True)
    
    @property
    def fornitore(self):
        return self.fornitore_set.all()
     
    def get_absolute_url(self):
        return reverse("anagrafica:vedifornitore", kwargs={"pk": self.pk})
    
    def __str__(self):
        return f'{self.ragioneSociale}'
    
    

class Privati(models.Model):
    nome_cognome=models.CharField(max_length=200)
    parente1=models.CharField(max_length=200, blank=True, null=True)
    parente2=models.CharField(max_length=200, blank=True, null=True)
    indirizzo=models.CharField(max_length=200)
    citta=models.CharField(max_length=200)
    provincia=models.CharField(max_length=2)
    cap=models.CharField(max_length=200)
    telefono_cliente=models.CharField(max_length=20)
    telefono_parente1=models.CharField(max_length=20,blank=True, null=True)
    telefono_parente2=models.CharField(max_length=20,blank=True, null=True)
    email=models.EmailField(blank=True, null=True)
    note=models.TextField(blank=True, null=True)
    installato=models.BooleanField(default=False, blank=True,null=True)

    @property
    def privato(self):
        return self.privato_set.all()
    
    def get_absolute_url(self):
        return reverse("anagrafica:vediprivato", kwargs={"pk": self.pk})
    
    def __str__(self):
        return f'{self.nome_cognome}'
    


    