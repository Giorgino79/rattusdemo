from django.shortcuts import render,redirect, get_object_or_404
from .models import Products,Warehouse, Order, Install
from .models import Azienda,Privati, Filiali
from .forms import ProdottoForm, OrderForm, RicevimentoOrdine, InstallForm, Primainstallazione,AggiornaInstallazione, MagazzinoMezzoForm
from io import BytesIO
from django.core.files.base import ContentFile
from django.template.loader import get_template
import os
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt
from automezzi.models import Automezzo, MagazzinoMezzo
from .forms import Carico
from django.utils import timezone


def prodotto(request):
    form=ProdottoForm(request.POST)
    if request.method=='POST':
       form=ProdottoForm(request.POST)
       if form.is_valid():
           obj=form.save(commit=False)
           obj.save()
           Warehouse.objects.create(prodotto=obj, giacenza=0).save()
           for a in Automezzo.objects.all():
               MagazzinoMezzo.objects.create(mezzo=a,prodotto=obj).save()
           messages.success(request,f'Nuovo prodotto inserito')
           return redirect('logistica:elencoprodotti')
    return render(request,'logistica/prodottoform.html', {'form':form})

def elencoprodotti(request):
    prodotti=Products.objects.all()            
    return render(request, 'logistica/elencoprodotti.html', {'p':prodotti})


    
def Vediprodotto(request,pk):
    prodotto=Products.objects.get(pk=pk)
    
    giacenza=Warehouse.objects.get(prodotto=prodotto)
        
    return render(request,'logistica/vediprodotto.html', {'c':prodotto,'giac':giacenza})
    
def Aggiornaprodotto(request, pk): #funzione aggiorna prodotto tasto in alto pagina vedi prodotto
    prodotto=Products.objects.get(pk=pk)
    form=ProdottoForm(instance=prodotto)
    if request.method=='POST':
        form=ProdottoForm(request.POST, instance=prodotto)
        if form.is_valid():
            form.save()
            return redirect('logistica:elencoprodotti')
    else:
        ProdottoForm()
    return render(request, 'logistica/prodottoform.html',{'form':form})

#ORDINI-----------------------------------------------------------

def nuovoordine(request):
    form=OrderForm(request.POST)
    if request.method=='POST':
       form=OrderForm(request.POST)
       if form.is_valid():
           form.save() 
           return redirect('logistica:ordinidaricevere')
    return render(request,'logistica/ordineform.html', {'form':form})

def vediordine(request,pk):
    ordine=Order.objects.get(pk=pk)
    return render(request,'logistica/vediordine.html',{'c':ordine})

def elencoordininonricevuti(request):
    ordini=Order.objects.all().filter(ricevuto=False)
    
    return render(request,'logistica/ordinidaricevere.html', {'ordini':ordini})

def elencoordiniricevuti(request):
    ordini=Order.objects.all().filter(ricevuto=True)
    
    return render(request,'logistica/ordiniricevuti.html', {'ordini':ordini})

def ordiniprodotto(request,pk):
    prodotto=Products.objects.get(pk=pk)
    ord=Order.objects.filter(prodotto=prodotto)
    ordine=ord.all()
    return render(request,'logistica/ordinisingoloprodotto.html', {'prodotto':prodotto,'ordini':ordine})

def inviaordinepdf(request,pk):
    ordine=Order.objects.get(pk=pk)
    user=get_user_model().objects.get(username=request.user)
    context={'c':ordine, 'user':user}
    response=BytesIO()
    template=get_template('logistica/pdfnuovoordine.html')
    html=template.render(context)
    pisa_status=pisa.CreatePDF(html,dest=response)
    response.seek(0)
    response=response.read()
    ordine.pdf=ContentFile(response,f'Ordine nr: {ordine.pk}')
    ordine.save()
    subject=f'Ordine nr: {ordine.pk}'
    body=f'Buongiorno {ordine.prodotto.fornitore.ragioneSociale},\n in allegato il ns. ordine relativo all acquisto del prodotto {ordine.prodotto.nome_prodotto}.\n Distinti saluti.\n {user.username}'
    mittente=settings.EMAIL_HOST_USER
    destinatario=ordine.prodotto.fornitore.mailOperativo1
    to=[destinatario]
    mail=EmailMultiAlternatives(subject,body,mittente,to)
    mail.attach_alternative(response,'application/pdf')
    mail.send()
    if mail:
        messages.success(request,f'Ordine nr: {ordine.pk} inviato correttamente al fornitore {ordine.prodotto.fornitore.ragioneSociale}')
    return redirect('logistica:ordiniricevuti')

def ordine_pdf(request, *args,**kwargs):
    pk=kwargs.get('pk')
    ordine=get_object_or_404(Order, pk=pk)
    template_path='logistica/pdfnuovoordine.html'
    context={'c':ordine}
    response=HttpResponse(content_type='application/pdf')
    response['Content-Dispositione']='filename="report.pdf"'
    template=get_template(template_path)
    html=template.render(context)
    pisa_status=pisa.CreatePDF(
        html, 
        dest=response
    )
    if pisa_status.err:
        return HttpResponse("C'è qualche problema <pre>"+html+'</pre>')
    return response

def ricezioneordine(request, pk):
    ordine=Order.objects.get(pk=pk)
    prodotto=Products.objects.get(pk=ordine.prodotto.pk)
    form=RicevimentoOrdine(request.POST, instance=ordine)
    if request.method=='POST':
        form=RicevimentoOrdine(request.POST, instance=ordine)
        if form.is_valid():
            obj=form.save(commit=False)    
            mag=Warehouse.objects.get(prodotto=ordine.prodotto)
            ricevuto=request.POST.get('articoli_ricevuti')
            giacenza=mag.giacenza+float(ricevuto)
            mag.giacenza=giacenza
            ordine.ricevuto=True
            ordine.importo_ordine=ordine.prezzo_singolo_articolo*float(ricevuto)
            ordine.save()
            mag.save()
            obj.save()
            return redirect('logistica:ordiniricevuti')
    return render(request,'logistica/ricezioneordine.html',{'ordine':ordine, 'form':form})

#MAGAZZINO---------------------------------
def magazzino(request):
    mag=Warehouse.objects.all()
    return render(request,'logistica/magazzino.html', {'mag':mag})



#CARICO MEZZI-------------------------------

def ScegliMezzo(request): 
    mezzo=Automezzo.objects.all()
    return render(request,'logistica/sceglimezzo.html',{'mezzo':mezzo})


#Installazioni-----------------------------

def installazione(request):
    form=InstallForm(request.POST)
    if request.method=='POST':
        form=InstallForm(request.POST)
        if form.is_valid():
            obj=form.save(commit=False)
            mezzo=request.POST['mezzo']
            azienda=request.POST['azienda']
            privato=request.POST['privato']
            filiale=request.POST['filiale']
            prodotto=request.POST.get('prodotto')
            quantità=request.POST.get('quantità')
            if azienda:
                cliente=Azienda.objects.get(pk=azienda)
                cliente.installato=True
                cliente.save()
            if privato:
                privati=Privati.objects.get(pk=privato)
                privati.installato=True
                privati.save()
            if filiale:
                filiali=Filiali.objects.get(pk=filiali)
                filiali.installato=True
                filiali.save()
            mezzo=Automezzo.objects.get(targa=mezzo)
            prod=Products.objects.get(pk=prodotto)
            carico=MagazzinoMezzo.objects.get(mezzo=mezzo, prodotto=prod)
            if carico.giacenza<quantità:
                raise ValidationError(f'Prodotto insufficiente, qualora fosse presente ci sono state omissioni o errori al carico del mezzo, farlo presente in ufficio per sistemare le giacenze')
            else:
                carico.giacenza-=quantità
                carico.save()
        
            obj.save()
            form=InstallForm()
            messages.success(request,f'Installazione inserita con successo')
            return redirect('logistica:installazione')
    return render(request, 'logistica/installazioni.html',{'form':form})

def vecchiainstallazione(request):
    form=InstallForm(request.POST)
    if request.method=='POST':
        form=InstallForm(request.POST)
        if form.is_valid():
            obj=form.save(commit=False)
            mezzo=request.POST['mezzo']
            azienda=request.POST['azienda']
            privato=request.POST['privato']
            filiale=request.POST['filiale']
            prodotto=request.POST.get('prodotto')
            quantità=request.POST.get('quantità')
            if azienda:
                cliente=Azienda.objects.get(pk=azienda)
                cliente.installato=True
                cliente.save()
            if privato:
                privati=Privati.objects.get(pk=privato)
                privati.installato=True
                privati.save()
            if filiale:
                filiali=Filiali.objects.get(pk=filiali)
                filiali.installato=True
                filiali.save()
            form=InstallForm()
            obj.save()
            messages.success(request,f'Installazione inserita con successo')
            return redirect('logistica:installazione')
    return render(request, 'logistica/vecchieinstallazioni.html',{'form':form})


def elencoinstallazioni(request):
    insta=Install.objects.all()
    return render(request, 'logistica/elencoinstallazioni.html',{'insta':insta})

def reportinstallazione(request,pk):
    installazione=Install.objects.get(pk=pk)
    user=get_user_model().objects.get(username=request.user)
    context={'i':installazione}
    return render(request,'logistica/pdfinstallazione.html',context)


def invioreportinstallazione(request,pk):
    installazione=Install.objects.get(pk=pk)
    user=get_user_model().objects.get(username=request.user)
    context={'i':installazione, 'user':user}
    template_path='logistica/pdfinstallazione.html'
    template=get_template(template_path)
    html=template.render(context)
    response=BytesIO()
    pisa_status=pisa.CreatePDF(html,dest=response)
    response.seek(0)
    response=response.read()
    installazione.pdf=ContentFile(response,f'Installazione nr: {installazione.pk}')
    installazione.save()
    subject=f'Report Installazione nr: {installazione.pk} del {installazione.data_installazione}'
    mittente=settings.EMAIL_HOST_USER
    body=f'In allegato il report per l installazione nr: {installazione.pk} effettuata in data: {installazione.data_installazione}'
    destinatario=installazione.azienda.mailOperativo1
    to=[destinatario]
    mail=EmailMultiAlternatives(subject,body,mittente,to)
    mail.attach_alternative(response,'application/pdf')
    mail.send()
    if mail:
        messages.success(request,f'Il report d installazione è stato inviato correttamente all indirizzo {installazione.azienda.mailOperativo1}')
    return redirect('logistica:elencoinstallazioni')
    
    
from django.core.exceptions import ValidationError
def aggiornainstallazione(request, pk):
    installazione=Install.objects.get(pk=pk)
    form=AggiornaInstallazione(request.POST, instance=installazione)
    if request.method=='POST':
        form=AggiornaInstallazione(request.POST, instance=installazione)
        if form.is_valid():
            obj=form.save(commit=False)
            prodotto=installazione.prodotto.pk
            quantità=request.POST.get('quantità')
            targa=request.POST['mezzo']
            cartelli=request.POST['cartelli']
            postazioni=request.POST['totale_postazioni']
            note=request.POST['note']
            mezzo=Automezzo.objects.get(targa=targa)
            prod=Products.objects.get(pk=prodotto)
            carico=MagazzinoMezzo.objects.get(mezzo=mezzo, prodotto=prod)
            if carico.giacenza<quantità:
                raise ValidationError(f'Prodotto insufficiente, qualora fosse presente ci sono state omissioni o errori al carico del mezzo, farlo presente in ufficio per sistemare le giacenze')
            else:
                carico.giacenza-=quantità
                carico.save()
            varia=installazione.quantità+float(quantità)
            installazione.quantità=varia
            installazione.data_installazione=timezone.now()
            installazione.cartelli=cartelli
            installazione.totale_postazioni=postazioni
            installazione.note=note
            installazione.save()
           
            messages.success(request,f'Installazione aggiornata con successo')
            return redirect('logistica:elencoinstallazioni')
            
    return render(request, 'logistica/agginstallazioni.html',{'form':form, 'insta':installazione})

#carico mezzi -----------------------------------
from django.db import transaction

def carica_mezzo(request,pk):
        mezzo=Automezzo.objects.get(pk=pk)
        scorte=Warehouse.objects.all()
        giacmezzo=MagazzinoMezzo.objects.filter(mezzo=mezzo).all()
        form=Carico()
        if request.method=='POST':
            form=Carico(request.POST)
            if form.is_valid():
                prodotto=form.cleaned_data['prodotto']
                quantita=form.cleaned_data['quantita']
                try:
                    with transaction.atomic():
                        furgone=MagazzinoMezzo.objects.get(mezzo=mezzo, prodotto=prodotto)
                        magazzino=Warehouse.objects.get(prodotto=prodotto)
                        
                        if magazzino.giacenza<quantita:
                            messages.error(request,'Non puoi caricare più prodotti di quanti disponibili in magazzino')
                            return redirect('logistica:caricamezzo', pk=mezzo.pk)
                        elif magazzino.giacenza<magazzino.soglia_giacenza:
                            aggiungi=furgone.giacenza+quantita
                            furgone.data_entrata=timezone.now()
                            furgone.giacenza=aggiungi
                            furgone.save()
                            messaggio_allerta=(f'Attenzione!!!! Soglia giacenza superata, avvisare ufficio per riordino merce, prodotti rimasti {magazzino.giacenza}')
                            messages.warning(request,messaggio_allerta)
                            togli=magazzino.giacenza-quantita
                            magazzino.giacenza=togli
                            magazzino.save()
                            messages.success(request,f'Caricati {quantita} {magazzino.prodotto.misura} del prodotto {magazzino.prodotto.nome_prodotto} sul mezzo {mezzo.targa}')
                            return redirect('logistica:caricamezzo', pk=mezzo.pk)
                        else:
                            aggiungi=furgone.giacenza+quantita
                            furgone.data_entrata=timezone.now()
                            furgone.giacenza=aggiungi
                            furgone.save()
                            togli=magazzino.giacenza-quantita
                            magazzino.giacenza=togli
                            magazzino.save()
                            messages.success(request,f'Caricati {quantita} {magazzino.prodotto.misura} del prodotto {magazzino.prodotto.nome_prodotto} sul mezzo {mezzo.targa}')
                except ValueError:
                    messages.error(request,'Inserisci una quantità valida')
            else:
                form=Carico()
        return render(request, 'logistica/carica_mezzo.html', {'form': form, 'scorte':scorte,  'mezzo':mezzo, 'giac':giacmezzo})


def vedimezzocarico(request,pk):
    mezzo=Automezzo.objects.get(pk=pk)
    mag=MagazzinoMezzo.objects.filter(mezzo=mezzo)
        
    return render(request, 'logistica/vedicarico.html', {'mezzo':mezzo, 'carichi':mag})