
from django.shortcuts import render, reverse, get_object_or_404, redirect
from .models import Servizio, Distinte,Recupero
from django.views.generic import FormView, ListView, UpdateView, DeleteView,View, TemplateView, DetailView
from django.http import HttpResponseRedirect, HttpResponse, FileResponse,Http404
from django.contrib import messages
from .forms import  ServizioAziende,ServizioPrivati, servizidelmese, chiudirecupero,salvaconferma, DistinteForm, chiudidistinta,chiudiservizio, cercaForm, ScegliCliente
from django.core.mail import send_mail
from anagrafica.models import Azienda, Privati,Filiali
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO, StringIO
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.urls import reverse_lazy
from django.db.models import F, Sum
import csv
from contabilità.models import Cassa,NumeroCassa
from automezzi.models import Automezzo,MagazzinoMezzo
from contratti.models import Contratto
from datetime import datetime
from io import FileIO, BytesIO
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from logistica.models import Products,Warehouse,Order
import datetime
from django.db.models import Q


def elencoservizi(request):
    
    form=cercaForm(request.POST or None)
    servizio=Servizio.objects.all()
    context={'servizio':servizio,'form':form}

    if request.method=='POST':
        servizio=Servizio.objects.filter(azienda__ragioneSociale__icontains=form['azienda'].value(),
                                         privati__nome_cognome__icontains=form['privati'].value(),
                                         Tiposervizio__icontains=form['Tiposervizio'].value()
                                         )
        if form['export_to_CSV'].value()==True:
            response=HttpResponse(content_type='text/csv')
            response['Content-Disposition']='attachment; filename="lista-magazzino.csv"'
            writer=csv.writer(response)
            writer.writerow(['CATEGORY', 'ITEM NAME', 'QUANTITY'])
            instance=servizio
            for servizio in instance:
                writer.writerow([servizio.azienda.ragioneSociale,servizio.id,servizio.privati])
                return response
        context={'servizio':servizio,'form':form}
        print(servizio)
    return render(request, 'servizi/elencoservizi.html', context)


def elencoservizipdf(request):
    form=servizidelmese((request.POST))
    if form.is_valid():
       datainizio=request.POST.get('data_inizio')
       datafine=request.POST.get('data_fine')
       cliente=request.POST['cliente']  
       if cliente:
           azienda=Azienda.objects.get(pk=cliente)
           qs=Servizio.objects.filter(azienda=azienda.pk)
           qs1=Servizio.objects.filter(Q(data_espletazione__gte=datainizio)).filter(azienda=azienda)
           qs2=Servizio.objects.filter(Q(data_espletazione__lte=datafine)).filter(azienda=azienda)
           a=qs.intersection(qs1,qs2)
           template_path='servizi/elencoservizipdf.html'
           context={'servizio':a, 'azienda':azienda}
           template=get_template(template_path)
           html=template.render(context)
           response=HttpResponse(content_type='application/pdf')
           response['Content-Disposition']='filename=Elenco Servizi'
           pisa_status=pisa.CreatePDF(html,dest=response)
           return response
           
    return render(request,'servizi/stampaservizipdf.html', {'form':form})
   
def vediservizio(request, pk):
    ser=Servizio.objects.get(pk=pk)  
    indirizzo=''
    if ser.azienda:
        indirizzo=f'{ser.azienda.indSedeLegale} + {ser.azienda.cittaLegale} + {ser.azienda.capLegale}'
    elif ser.privati:
        indirizzo=f'{ser.privati.indirizzo} + {ser.privati.citta} + {ser.privati.cap}'
    else:
        indirizzo=f'{ser.filiali.indFiliale} + {ser.filiali.cittaFiliale} + {ser.filiali.capFiliale}'
    return render(request,'servizi/vediservizio.html',{'c':ser,'indirizzo':indirizzo})

def nuovoservizio(request):
        return render(request, 'servizi/sceltacliente.html')

def sceglicliente(request):
    azienda=Azienda.objects.all()
    form=ScegliCliente(request.POST)
    if request.method=='POST':
        form=ScegliCliente(request.POST)
        if form.is_valid:
            azienda=request.POST['ragioneSociale']
            prendi=Azienda.objects.get(pk=azienda)
            vai=prendi.pk
            return redirect('servizi:servizioaziende', pk=vai )
    return render(request,'servizi/sceglicliente.html', {'form':form})


def nuovoservizioaziende(request, pk):
    azienda=Azienda.objects.get(pk=pk)
    form=ServizioAziende(azienda=azienda) 
    if request.method=='POST':
        form=ServizioAziende(request.POST)
        if form.is_valid():
            obj=form.save(commit=False)
            contratto=request.POST['contratto']
            filiali=request.POST['filiali']
            data_servizio=request.POST['data_espletazione']
            altro_luogo=request.POST['altro_luogo']
            prezzo=request.POST['prezzo']
            tiposerv=request.POST['Tiposervizio']
            prodotto=request.POST.get('prodotto')
            note=request.POST['note']
            orario=request.POST['orario_inizio']
            if prodotto==None or prodotto=='':
                pass
            else:
                prodotto=Products.objects.get(pk=prodotto)
            
                if contratto:
                        contract=Contratto.objects.get(pk=contratto)
                        if filiali == None or filiali=='':
                            
                            servizio=Servizio.objects.create(
                                    azienda=azienda, 
                                    contratto=contract,
                                    filiali=None,
                                    data_espletazione=data_servizio,
                                    altro_luogo=altro_luogo,
                                    prezzo=0,
                                    Tiposervizio=tiposerv,
                                    prodotto=prodotto,
                                    note=note,
                                    orario_inizio=orario
                                    ).save()
                        else:
                            filiali=Filiali.objects.get(pk=filiali)
                            
                            servizio=Servizio.objects.create(
                                    azienda=azienda, 
                                    contratto=contract,
                                    filiali=filiali,
                                    data_espletazione=data_servizio,
                                    altro_luogo=altro_luogo,
                                    prezzo=0,
                                    Tiposervizio=tiposerv,
                                    prodotto=prodotto,
                                    note=note,
                                    orario_inizio=orario
                                    ).save()
                        
                else:    
                            contratto=None
                            filiali=None           
                            servizio=Servizio.objects.create(
                            azienda=azienda, 
                            contratto=None,
                            filiali=None,
                            data_espletazione=data_servizio,
                            altro_luogo=altro_luogo,
                            prezzo=prezzo,
                            Tiposervizio=tiposerv,
                            prodotto=prodotto,
                            note=note,
                            orario_inizio=orario
                            ).save()
                
            messages.success(request,f'Servizio inserito')
            form=ServizioAziende()
            return redirect('servizi:sceglicliente')
    return render(request,'servizi/servizioaziende.html',{'form':form})

def servizioprivati(request):
    template_name='servizi/servizioprivati.html'
    form=ServizioPrivati(request.POST)
    if request.method=='POST':
        form=ServizioPrivati(request.POST)
        if form.is_valid():
            obj=form.save(commit=False)
            privato=request.POST.get('privati')
            data_espletazione=request.POST.get('data_espletazione')
            altroluogo=request.POST.get('altro_luogo')
            prezzo=request.POST.get('prezzo')
            incasso=request.POST.get('incasso')
            tiposervizio=request.POST.get('Tiposervizio')
            prodotto=request.POST.get('prodotto')
            note=request.POST.get('note')
            orario=request.POST.get('orario_inizio')
            if altroluogo=='' or altroluogo==None:
                altroluogo=None 
            if incasso == None:
                incasso=0
            cliente=Privati.objects.get(pk=privato)
            prod=Products.objects.get(pk=prodotto)
            servizio=Servizio.objects.create(
                privati=cliente, 
                data_espletazione=data_espletazione,
                altro_luogo=altroluogo,
                prezzo=prezzo,
                incasso=incasso,
                Tiposervizio=tiposervizio,
                prodotto=prod,
                note=note,
                orario_inizio=orario,   
            ).save()
        return redirect('servizi:sceglicliente')
    return render(request, template_name,{'form':form})
            
            
    
    

def aggservizioazienda(request,pk):
    azienda=Servizio.objects.get(pk=pk)
    form=ServizioAziende(instance=azienda)
    if request.method=='POST':
       form=ServizioAziende(request.POST,instance=azienda)
       if form.is_valid():
           form.save()
           messages.success(request,'Servizio nr: ' + str(azienda.pk) + ' aggiornato')
           return redirect('servizi:elencoservizi')
    return render(request, 'servizi/aggiornaservizioaziende.html',{'form':form})

def aggservizioprivati(request,pk):
    privati=Servizio.objects.get(pk=pk)
    form=ServizioPrivati(instance=privati)
    if request.method=='POST':
       form=ServizioPrivati(request.POST,instance=privati)
       if form.is_valid():
           form.save()
           messages.success(request,'Servizio nr: ' + str(privati.pk) + ' aggiornato')
           return redirect('servizi:elencoservizi')
    return render(request, 'servizi/aggiornaservizioprivati.html',{'form':form})



def pdfconferma(request,pk):
    servizio=get_object_or_404(Servizio,pk=pk)
    template_path='servizi/pdfconfermaprivati.html'
    user=get_user_model().objects.get(username=request.user)
    context={'s':servizio, 'user':user}
    # response=HttpResponse(content_type='application/pdf')
    # response['Content-Disposition']='filename="report.pdf"'
    response=BytesIO()
    template=get_template(template_path)
    html=template.render(context)
    pisa_status=pisa.CreatePDF(
        html,
        dest=response
        
    )
    response.seek(0)
    response=response.read()
    email_content=render_to_string('servizi/pdfconfermaprivati.html', context)
    servizio.pdf=ContentFile(response,f'Servizio nr: {servizio.pk}')
    servizio.save()
    subject=f'Report servizio nr.: {servizio.pk}'
    body=f'In allegato il report per il servizio nr: {servizio.pk} effettuato in data: {servizio.data_espletazione}'
    mittente=settings.EMAIL_HOST_USER
    to=[servizio.azienda.mailOperativo1]
    mail=EmailMultiAlternatives(subject,body,mittente,to)
    mail.attach_alternative(response,'application/pdf')
    mail.send()
    if mail:
        messages.success(request, f'il report per il servizio nr: {servizio.pk} è stato inoltrato correttamente alla mail: {to}')
    else:
        messages.error(request, "C'è qualche problema")
    return redirect('servizi:elencoservizi')
    


def cancellaservizio(request,pk):
    
    oggetto=Servizio.objects.get(pk=pk)
    if request.method=='POST':
        oggetto.delete()
        messages.success(request, 'Servizio Cancellato')
        return redirect('servizio:elencoservizi')
    return render(request, 'servizi/cancellaservizio.html', {'o':oggetto})

def pdf_view(request,pk):
    pdf=Servizio.objects.get(pk=pk)
    pdf_file=pdf.pdf
    
    try:
        return FileResponse(pdf_file.open('rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()

########################DISTINTE##################         

class DistintaInserisci(FormView):
     form_class=DistinteForm
     template_name='servizi/nuovadistinta.html'
     
     def get_queryset(self):
         queryset=super().get_queryset()
         return queryset.filter(servizio_espletato=False)
     
     def get_success_url(self):
            return reverse('servizi:vedidistinta', args=[self.i_instance.pk]) 
       
     def form_valid(self, form):
        self.i_instance = form.save()
        messages.add_message(self.request, messages.INFO, f"Distinta: {self.i_instance.id} inserita")
        return super().form_valid(form)
    
    
     def form_invalid(self, form):
        print(form.errors)
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)
    
    


def elencodistinte(request):
    elenco=Distinte.objects.filter(chiusura=False)
    return render(request, 'servizi/elencodistinte.html',{'el': elenco})

def elencodistintechiuse(request):
    elenco=Distinte.objects.filter(chiusura=True)
    return render(request, 'servizi/distintechiuse.html',{'el': elenco})
    
def aggiornadistinta(request,pk):
    
    distinta=Distinte.objects.get(pk=pk)
    form=DistinteForm(instance=distinta)
    if request.method=='POST':
        form=DistinteForm(request.POST, instance=distinta)
        if form.is_valid():
            form.save()
            messages.success(request,'Servizio nr: ' + str(distinta.pk) + ' aggiornato')

        return redirect('servizi:elencodistinte')
    return render(request, 'servizi/aggiornadistinta.html',{'form':form, 'distinta':distinta})

def cancelladist(request,pk):
    oggetto=Distinte.objects.get(pk=pk)
    if request.method=='POST':
        riapriservizi=oggetto.servizio.all()
        for r in riapriservizi:
            r.inespl=False
            r.save()
        oggetto.delete()
        messages.success(request,'Distinta cancellata')
        return redirect('servizi:elencodistinte')
    return render(request, 'servizi/cancelladistinta.html', {'o':oggetto})


from django.core.exceptions import ValidationError
def chiudiserv(request,pk):
    servizio=Servizio.objects.get(pk=pk)
    prezzo=servizio.prezzo
    distinta=Distinte.objects.get(servizio=servizio)
    auto=distinta.automezzo.pk
    mezzo=Automezzo.objects.get(pk=auto)
    form=chiudiservizio(instance=servizio)
    if request.method=='POST':
        #form per chiusura servizio
        form=chiudiservizio(request.POST, instance=servizio)
        if form.is_valid():
            obj=form.save(commit=False)
            prodotto=request.POST.get('prodotto')
            quantità=request.POST.get('quantità')
            espletato=request.POST['espletato']
            importo=request.POST.get('importo_incassato')
            if espletato:
                servizio.espletato=True
                servizio.save()
            else:
                servizio.esplato=False
                servizio.inespl=False
                servizio.save()
            if prodotto:
                prodotto=Products.objects.get(pk=prodotto)
                furgone=MagazzinoMezzo.objects.get(mezzo=mezzo, prodotto=prodotto.pk)
                if furgone.giacenza<float(quantità):
                     raise ValidationError(f'Prodotto insufficiente, qualora fosse presente ci sono state omissioni o errori al carico del mezzo, farlo presente in ufficio per sistemare le giacenze')
                else:
                    furgone.giacenza-=float(quantità)
                    furgone.save()
                if prodotto and distinta and mezzo:
                    messages.success(request,'oggetti presi')
                else:
                    messages.error(request,'oggetti non capati')
            if servizio.contratto:
                pass    
            else:
                importo=request.POST['importo_incassato']
                if importo !=0 and servizio.incasso==False:
                    cassa=NumeroCassa.objects.get(pk=1)
                    data=datetime.datetime.now()
                    if importo==servizio.prezzo:
                        servizio.incasso=True
                        servizio.save()
                    registra=Cassa.objects.create(numero_cassa=cassa,servizio=servizio, cassadare=importo, data=data)
                    registra.save()
                else:
                    pass
                
                

            #chiuso il servizio creo eventuale recupero crediti
            if importo == '' or importo=='0.00':
                pass
            elif importo != servizio.prezzo:
                darec=servizio.prezzo-float(importo)
                recupero=Recupero.objects.create(servizio=servizio, importo_da_recuperare=darec)
                recupero.save()
            else:
                pass
            
            obj.save()
            form=chiudiservizio()
            return redirect('servizi:vedidistinta', pk=distinta.pk)
    return render(request, 'servizi/chiudiservizio2.html',{'form':form, 'servizio':servizio,'prezzo':prezzo})


def vedidistinta2(request, pk):
    dist=Distinte.objects.get(pk=pk)    
    servdist=dist.servizio.all()
    sommaservizi=servdist.aggregate(c=Sum('prezzo'))
    recupero=dist.recupero.all()
    sommarecupero=recupero.aggregate(c=Sum('importo_da_recuperare'))
    servizi=dist.servizio.count()
    servizio=dist.servizio.all().update(inespl=True)
    espletato=dist.servizio.filter(espletato=False)
    indirizzo=''
    for ser in servdist:
        if ser.azienda:
            indirizzo=f'{ser.azienda.indSedeLegale} + {ser.azienda.cittaLegale} + {ser.azienda.capLegale}'
        elif ser.privati:
            indirizzo=f'{ser.privati.indirizzo} + {ser.privati.citta} + {ser.privati.cap}'
        else:
            indirizzo=f'{ser.filiali.indFiliale} + {ser.filiali.cittaFiliale} + {ser.filiali.capFiliale}'
    context={'c':dist,'e':espletato,'r':recupero, 'sommaservizi':sommaservizi,'sommarecupero':sommarecupero,'servizi':servizi,'indirizzo':indirizzo}
    return render(request,'servizi/vedidistinta.html',context)

def chiudirecuperoview(request,pk):
    recupero=Recupero.objects.get(pk=pk)
    form =chiudirecupero(request.POST, instance=recupero)
    servizio=Servizio.objects.get(pk=recupero.servizio.pk)
    if request.method=='POST':
        form=chiudirecupero(request.POST, instance=recupero)
        if form.is_valid():
            form.save()
            importo=recupero.importo_da_recuperare
            recupero.chiuso=True
            recupero.data_chiusura=datetime.datetime.now()
            recupero.save()
            servizio.incasso=True
            servizio.save()
            numcassa = NumeroCassa.objects.get(pk=1)
            cassa=Cassa.objects.create(numero_cassa=numcassa, causale='Recupero nr. '+str(recupero.pk), 
                                       servizio=servizio, data=datetime.datetime.now(), cassadare=importo )
            cassa.save()
            return redirect('servizi:elencodistinte')
    return render(request, 'servizi/chiudirecupero.html',{'form':form})

def chiudidist(request, pk):
    
    distinta=Distinte.objects.get(pk=pk)   
    
    form=chiudidistinta(request.POST, instance=distinta)
    if request.method=='POST':
        form=chiudidistinta(request.POST, instance=distinta)
        if form.is_valid():
            form.save()         
          
        return redirect('home:home')
    context={'form':form,'distinta':distinta}
    return render(request,'servizi/chiudidistinta.html', context)



def chiudiserv2(request,pk):
    servizio=Servizio.objects.get(pk=pk)
    prezzo=servizio.prezzo
    distinta=Distinte.objects.get(servizio=servizio)
    auto=distinta.automezzo.pk
    mezzo=Automezzo.objects.get(pk=auto)
    form=chiudiservizio(instance=servizio)
    if request.method=='POST':
        #form per chiusura servizio
        form=chiudiservizio(request.POST, instance=servizio)
        if form.is_valid():
            obj=form.save(commit=False)
            prodotto=request.POST.get('prodotto')
            quantità=request.POST.get('quantità')
            espletato=request.POST['espletato']
            importo=request.POST.get('importo_incassato')
            if espletato:
                servizio.espletato=True
                servizio.save()
            else:
                servizio.esplato=False
                servizio.inespl=False
                servizio.save()
            if prodotto:
                prodotto=Products.objects.get(pk=prodotto)
                furgone=MagazzinoMezzo.objects.get(mezzo=mezzo, prodotto=prodotto.pk)
                if furgone.giacenza<float(quantità):
                     raise ValidationError(f'Prodotto insufficiente, qualora fosse presente ci sono state omissioni o errori al carico del mezzo, farlo presente in ufficio per sistemare le giacenze')
                else:
                    furgone.giacenza-=float(quantità)
                    furgone.save()
                if prodotto and distinta and mezzo:
                    messages.success(request,'oggetti presi')
                else:
                    messages.error(request,'oggetti non capati')
            #gestiamo l'incasso ma non lo mettiamo in cassa, in cassa ci andrà tramite chiusura distinta
            #chiuso il servizio creo eventuale recupero crediti
            if servizio.incasso:
                if importo != servizio.prezzo:
                    darec=servizio.prezzo-float(importo)
                    recupero=Recupero.objects.create(servizio=servizio, importo_da_recuperare=darec)
                    recupero.save()
                elif importo == servizio.prezzo:
                    servizio.incasso=True
                    servizio.save()
                else:
                    pass
                print(importo, recupero)
            
            obj.save()
            form=chiudiservizio()
            return redirect('servizi:vedidistinta', pk=distinta.pk)
    return render(request, 'servizi/chiudiservizio2.html',{'form':form, 'servizio':servizio,'prezzo':prezzo})



def chiudiincassidistinta(request,pk):
    distinta=Distinte.objects.get(pk=pk)
    incassi=distinta.servizio.all()
    form = chiudidistinta(instance=distinta)
    if request.method=='POST':
        form = chiudidistinta(request.POST, instance=distinta)
        if form.is_valid():
            obj=form.save(commit=False)
            cassa=request.POST.get('cassa')
            caxa=NumeroCassa.objects.get(pk=cassa)
            for inc in incassi:
                servizio=Servizio.objects.get(pk=inc.pk)
                registra=Cassa.objects.create(
                    numero_cassa=caxa,
                    servizio=servizio, 
                    cassadare=servizio.importo_incassato, 
                    data=datetime.datetime.now()).save()
            obj.save()
            return redirect('servizi:elencodistinte')
        else:
            form=chiudidistinta()
    context={'form':form,'distinta':distinta}
    return render(request, 'servizi/chiudidistinta.html', context)
        
                