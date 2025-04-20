from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,get_object_or_404, redirect
from django.urls import reverse_lazy
from servizi.models import Servizio, Distinte, Recupero
from .models import Cassa, Banca,BancaMovimenti, FatturaAttiva,FatturaPassiva, Movimenti, NumeroCassa
from django.db.models import Count, Sum, FloatField, DecimalField, F
from django.db.models.functions import Cast
from .forms import RecuperoForm, Chiudirecupero, AggiornaRecupero,BancaForm,Elencoserviziperfattura, NumeroCassaForm, Versa, MovimentiForm, FatturaAttivaForm,FatturaPassivaForm
from django.http import HttpResponseRedirect    
from django.views.generic import FormView, ListView, UpdateView
from django.urls import reverse
from anagrafica.models import Fornitori,Azienda,Privati
from django.template.loader import get_template
from xhtml2pdf import pisa
from contratti.models import Contratto
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from logistica.models import Order
from django.core.files import File
from django.core.files.base import ContentFile
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib import messages
from django.http import FileResponse
from anagrafica.models import Azienda
from django.db.models import Q
from io import BytesIO
import csv   
from django.http import HttpResponse     

def incassi(request):#app in disuso, si utilizza vedirecuperi, tenuta solo per le belle sintassi
    servizi=Servizio.objects.filter(incasso=False).filter(espletato=True)
    daincassare=Servizio.objects.filter(incasso=False).annotate(d=F('prezzo')-F('importo_incassato'), output_field=FloatField())#filtro i servizi chiusi senza incasso e 
    #faccio la differenza fra quanto si doveva incassare e quanto è stato incassato, 
    #poi posso richiamarlo nel for della tabella come le altre voci i.variabile con cui ho chiamato la funzione f
    totale=daincassare.aggregate(tot=Sum('d'), output_field=FloatField())# con il queryset daincassare sommo tutto il mancato incasso per la tfoot della tabella
    
    totprezzo=Servizio.objects.filter(incasso=False).annotate(c=F('prezzo'))#queryset dei servizi non chiusi con la spunta dell incasso
    totaleprezzo=totprezzo.aggregate(tp=Sum('c')) #con il queryset totprezzo sommo tutto quanto si doveva incassare per il tfoot della tabella
    
    incasso=Servizio.objects.filter(incasso=False).annotate(i=F('importo_incassato'))#recupero gli importi incassati dai servizi 
    #chiusi senza incasso
    totincasso=incasso.aggregate(inc=Sum('i'))#sommo gli importi dei servizi senza incasso
    
    recuperi=Recupero.objects.all()
    
    
    return render(request, 'contabilità/daincassare.html',{'somma':totale, 'recuperi':recuperi,'dainc':daincassare,
                                                           'tot':totincasso,'el':totaleprezzo, 'inc':servizi})

def crearecupero(request, pk):# app in disuso, si fa in automatico con la chiusura del servizio
    servizio=Servizio.objects.get(pk=pk)
    form=RecuperoForm(request.POST,instance=servizio)
    if request.method =='POST':
       form=RecuperoForm(request.POST,instance=servizio)
       if form.is_valid():
           form.save()
           return redirect('contabilità:elencorecupero')
    else:
        RecuperoForm()
    return render(request, 'contabilità/nuovorecupero.html',{'form':form, 'ser':servizio})
    
def vedirecupero(request,pk):
    recupero=Recupero.objects.get(pk=pk)
    return render(request,'contabilità/vedisingolorecupero.html',{'rec':recupero})

    

def vedirecuperi(request):
    recupero=Recupero.objects.filter(chiuso=False)
    return render(request,'contabilità/elencorecuperi.html',{'rec':recupero})

def aggiornarecupero(request,pk):
    recupero=get_object_or_404(Recupero, pk=pk)
    form=RecuperoForm(request.POST, instance=recupero)
    if request.method=='POST':
        form=RecuperoForm(request.POST, instance=recupero)
        if form.is_valid():
            obj=form.save(commit=False)
            chiuso =request.POST['chiuso']
            importo=request.POST['importo_da_recuperare']
            note=request.POST['note']
            data=request.POST['data']
            datachiuso=request.POST['data_chiusura']
            numerocassa=NumeroCassa.objects.get(pk=1)
            if chiuso:
                obj.chiuso=True
                obj.data=data
                obj.data_chiusura=datachiuso
                cassa=Cassa.objects.create(causale=note, cassadare=importo, data=datetime.now(), numero_cassa=numerocassa)
                
                cassa.save()
                obj.save()
                return redirect('contabilità:elencorecupero')
    context={'form':form, 'recupero':recupero}
    return render(request,'contabilità/aggiornarecupero.html', context)


def chiudiincasso(request, pk):
    recupero=Recupero.objects.get(pk=pk)
    servizio=Servizio.objects.get(pk=recupero.servizio.pk)
    form=Chiudirecupero(request.POST, instance=recupero)
    if request.method=='POST':
        form=Chiudirecupero(request.POST, instance=recupero)
        if form.is_valid():
            cassa=form.save(commit=False)                
            servizio=Servizio.objects.get(pk=recupero.servizio.pk)
            importo=request.POST['importo']
            registra=Cassa.objects.create(servizio=servizio,cassadare=int(importo))
            registra.save()
            cassa.save()
            return redirect('contabilità:elencorecupero')
    return render(request,'contabilità/chiudirecupero.html', {'form':form,'recupero':recupero, 'servizio':servizio})

def vedicassa(request):
    cassa=Cassa.objects.all()
    avere=Cassa.objects.aggregate(avere=Sum('cassaavere'))
    dare=Cassa.objects.aggregate(dare=Sum('cassadare'))
    totale=Cassa.objects.aggregate(tot=(Sum('cassadare', output_field=FloatField())-Sum('cassaavere', output_field=FloatField())))
    
    return render(request, 'contabilità/cassa.html',{'cassa':cassa,'avere':avere,'dare':dare, 'totale':totale})
        
class Bancanuova(LoginRequiredMixin,FormView):
    form_class=BancaForm
    template_name='contabilità/nuovabanca.html'
    success_url=reverse_lazy('contabilità:elencobanche')
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class CassaNuova(LoginRequiredMixin,FormView):
    form_class=NumeroCassaForm
    template_name='contabilità/nuovacassa.html'
    success_url=reverse_lazy('home:home')
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
     
def elencobanche(request):
    qs=Banca.objects.all()
    return render(request,'contabilità/elencobanche.html', {'qs':qs})
    
class AggiornaAnagraficaBanca(UpdateView):
    form_class=BancaForm
    template_name='contabilità/aggiornaanagraficabanca.html'
    success_url=reverse_lazy('contabilità:elencobanche')
    

    
   
def movimenti(request):
    form=MovimentiForm(request.POST)
    if request.method=="POST":
        form=MovimentiForm(request.POST)
        if form.is_valid():
            obj=form.save(commit=False)
            data=request.POST.get('data')
            causale=request.POST.get('causale')
            banca=request.POST.get('banca')
            importo=request.POST.get('importo')
            cassa=request.POST.get('cassa')
            fattura_passiva=request.POST.get('fattura_passiva')
            fattura_attiva=request.POST.get('fattura_attiva')
            obj.data=data
            obj.causale=causale
            obj.importo=importo
            if fattura_attiva:
                attiva=FatturaAttiva.objects.get(pk=fattura_attiva)
                if banca:
                    bancarif=Banca.objects.get(pk=banca)        
                    attiva.da_incassare=False
                    attiva.data_pagamento=data
                    attiva.avere=importo
                    attiva.save()
                    b=BancaMovimenti.objects.create(banca=bancarif, causale=causale, data=data, dare=importo,avere=0,fatturaattiva=attiva)
                    b.save()
                elif cassa:
                    cassarif=NumeroCassa.objects.get(pk=cassa)
                    attiva.da_incassare=False
                    attiva.data_pagamento=data
                    attiva.avere=importo
                    attiva.save()
                    c=Cassa.objects.create(numero_cassa=cassarif,causale=causale, data=data, cassadare=importo, cassaavere=0,fatturaattiva=attiva)
                    c.save()
                else:
                  pass
            if fattura_passiva:
                passiva=FatturaPassiva.objects.get(pk=fattura_passiva)
                passiva.data_pagamento=data
                passiva.dare=importo
                passiva.da_pagare=False
                passiva.save()
                ordini=passiva.ordini_acquisto.all()
                for o in ordini:
                    order=Order.objects.filter(pk=o.pk)
                    for i in order:
                        i.pagato=True
                        i.save()
                if banca:
                    bancarif=Banca.objects.get(pk=banca)        
                    b=BancaMovimenti.objects.create(banca=bancarif, causale=causale, data=data, avere=importo, dare=0, fatturapassiva=passiva)                                
                    b.save()
                elif cassa:
                    cassarif=NumeroCassa.objects.get(pk=cassa)
                    c=Cassa.objects.create(numero_cassa=cassarif,causale=causale, data=data, cassaavere=importo, cassadare=0, fatturapassiva=passiva)     
                    c.save()
                else:
                     pass
            obj.save()
            form=MovimentiForm()
    return render(request,'contabilità/movimenti.html',{'form':form})

def vedimovimentibanca(request,pk):
    ban=get_object_or_404(Banca,pk=pk)
    banca=BancaMovimenti.objects.filter(banca=ban.pk) 
    avere=banca.aggregate(avere=Sum('avere'))
    dare=banca.aggregate(dare=Sum('dare'))
    totale=dare['dare']-avere['avere']  
    return render(request,'contabilità/vedibanca.html',{'banca':banca,'ban':ban,'avere':avere,'dare':dare, 'totale':totale})

            
def prelievo(request):
    form=Versa(request.POST)
    if request.method=='POST':
        form=Versa(request.POST)
        if form.is_valid():
            obj=form.save(commit=False)
            banca=request.POST['banca']
            cassa=request.POST['cassa']
            data=request.POST['data']
            casuale=request.POST['casuale']
            importo=request.POST['importo']
            pdf=request.POST['aggiungifile']
            numerocassa=NumeroCassa.objects.get(pk=cassa)
            numerobanca=Banca.objects.get(pk=banca)
            entra=Cassa.objects.create(numero_cassa=numerocassa, casuale=casuale, data=data, cassadare=importo,aggiungifile=pdf)
            entra.save()
            esce=BancaMovimenti.objects.create(banca=numerobanca, casuale=casuale,data=data,avere=importo,aggiungifile=pdf)
            esce.save()
            obj.save()
            form=Versa()
    return render(request,'contabilità/prelievi.html', {'form':form})

def versamento(request):
    form=Versa(request.POST)
    if request.method=='POST':
        form=Versa(request.POST)
        if form.is_valid():
            obj=form.save(commit=False)
            banca=request.POST['banca']
            cassa=request.POST['cassa']
            data=request.POST['data']
            causale=request.POST['causale']
            importo=request.POST['importo']
            pdf=request.POST['aggiungifile']
            numerocassa=NumeroCassa.objects.get(pk=cassa)
            numerobanca=Banca.objects.get(pk=banca)
            entra=Cassa.objects.create(numero_cassa=numerocassa, causale=causale, data=data, cassaavere=importo,aggiungifile=pdf)
            entra.save()
            esce=BancaMovimenti.objects.create(banca=numerobanca, causale=causale,data=data,dare=importo,aggiungifile=pdf)
            esce.save()
            obj.save()
            form=Versa()
            messages.success(request,f'Versamento registrato con successo')
    return render(request,'contabilità/versamento.html', {'form':form})



def vedimovimentibanca(request,pk):
    
    banca=Banca.objects.get(pk=pk)
    mov=BancaMovimenti.objects.filter(banca=banca)
    d=BancaMovimenti.objects.filter(banca=banca).annotate(i=F('dare'))
    dare=d.aggregate(inc=Sum('i'))
    a=BancaMovimenti.objects.filter(banca=banca).annotate(i=F('avere'))
    avere=a.aggregate(inc=Sum('i'))
    saldo=BancaMovimenti.objects.aggregate(s=Sum('dare')-Sum('avere'))
    return render(request, 'contabilità/vedibanca.html', {'nome':banca,'banca':mov,'avere':avere,'dare':dare,'saldo':saldo})

#fatturazione-------------------------------------
    
class FatturaPassivaView(FormView):
    form_class=FatturaPassivaForm
    template_name='contabilità/nuovafatturapassiva.html'
    success_url=reverse_lazy('contabilità:elencofatturepassive')
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)



def elencofattureattive(request):
    fatture=FatturaAttiva.objects.all().order_by('data_fattura')
    return render(request, 'contabilità/elencofattureattive.html',{'fatture':fatture})


def vedipdf(request,pk):
    fattura=FatturaAttiva.objects.get(pk=pk)
    template_path='contabilità/fatturachatgpt.html'
    
    context={'s':fattura}
    response=HttpResponse(content_type='application/pdf')
    response['Content-Disposition']='filename="report.pdf"'
    template=get_template(template_path)
    html=template.render(context)
    pisa_status=pisa.CreatePDF(
        html,
            dest=response
        )
    if pisa_status.err:
            return HttpResponse("C'è qualche problema <pre>"+html+'</pre>')
    return response
            

def elencofatturepassive(request):
    fatture=FatturaPassiva.objects.filter(da_pagare=True).order_by('data_fattura')
   
    return render(request, 'contabilità/elencofatturepassive.html',{'fatture':fatture})



def scegliclientefattura(request):
    cliente=Azienda.objects.all()
    return render(request,'contabilità/scegliclienteperfattura.html', {'cliente':cliente})
    
def fatturacliente(request, pk):
    cliente=Azienda.objects.get(pk=pk)
    form=Elencoserviziperfattura(request.POST)
    if request.method=='POST':
        form=Elencoserviziperfattura(request.POST)
        if form.is_valid():
                datainizio=request.POST.get('data_inizio')
                datafine=request.POST.get('data_fine')
                cliente=request.POST['cliente']
                forn=request.POST.get('fornitore')
                qs=Servizio.objects.filter(azienda=cliente.pk)
                qs1=Servizio.objects.filter(Q(data_espletazione__gte=datainizio)).filter(azienda=cliente)
                qs2=Servizio.objects.filter(Q(data_espletazione__lte=datafine)).filter(azienda=cliente)
                a=qs.intersection(qs1,qs2)
                response=BytesIO()
                context={'a':a,'cliente':cliente}
                template_path='contabilità/fatturachatgpt.html'
                html=get_template(template_path)
                pisa_satus=pisa.CreatePDF(html,dest=response)
                
                
                
    
    
    
def invio_fattura_pdf(request, pk):
    fattura=get_object_or_404(FatturaAttiva, pk=pk)
    template_path='contabilità/pdffattura.html'
    context={'c':fattura}
    # response=HttpResponse(content_type='application/pdf')
    # response['Content-Dispositione']='filename="report.pdf"'
    response=BytesIO()
    template=get_template(template_path)
    html=template.render(context)
    pisa_status=pisa.CreatePDF(
        html,
        dest=response
    )
    response.seek(0)
    response=response.read()
    fattura.pdf=ContentFile(response,f'Fattura nr: {fattura.pk}')
    fattura.save()
    subject=f'Invio fattura nr: {fattura.pk} del {fattura.data_fattura}'
    body=f'Buongiorno {fattura.azienda.ragioneSociale},\n in allegato trova il tabulato dei servizi espletati il mese scorso, per qualsiasi esigenza o problema non esitate a chiamarci.\n Distinti saluti.\n ggiSoftware'
    mittente=settings.EMAIL_HOST_USER
    to=['danigioloso@gmail.com']
    mail=EmailMultiAlternatives(subject,body,mittente,to)
    mail.attach_alternative(response,'application/pdf')
    mail.send()
    if mail:
        messages.success(request, f'Fattura nr: {fattura.pk} inviata correttamente all indirizzo {to}')
    else:
        messages.error(request, "C'è qualche problema")    
    return redirect('contabilità:elencofattureattive')


def fatturazione(request):
    form=FatturaAttivaForm(request.POST)
    if request.method=='POST':
        form=FatturaAttivaForm(request.POST)
        if form.is_valid():
            obj=form.save(commit=False)            
            imponibile=request.POST['imponibile']
            iva=float(imponibile)*0.22
            obj.importoiva=iva
            obj.totale=obj.imponibile+obj.importoiva
            obj.save()
            form=FatturaAttivaForm()
    return render(request,'contabilità/nuovafatturaattiva.html',{'form':form})


def mese(request):
    form=Elencoserviziperfattura(request.POST)
    if form.is_valid():
        datainizio=request.POST.get('data_inizio')
        datafine=request.POST.get('data_fine')
        cliente=request.POST['cliente']
        forn=request.POST.get('fornitore')
        if cliente:
            azienda=Azienda.objects.get(pk=cliente)
            qs=Servizio.objects.filter(azienda=azienda.pk)
            qs1=Servizio.objects.filter(Q(data_espletazione__gte=datainizio)).filter(azienda=azienda)
            qs2=Servizio.objects.filter(Q(data_espletazione__lte=datafine)).filter(azienda=azienda)
            a=qs.intersection(qs1,qs2)
            response=HttpResponse('text/csv')
            response['Content-Disposition']='attachment;filename=elencoservizi.csv'
            writer=csv.writer(response)
            writer.writerow(['Numero Servizio', 'Cliente','Data', 'Natura del Servizio','Imponibile'] )
            servizio=a.values_list('id', 'azienda__ragioneSociale','data_espletazione','Tiposervizio','prezzo')
            for serv in servizio:
                writer.writerow(serv)
            return response
        if forn:
            fornitore=Fornitori.objects.get(pk=forn)
            elenco=Order.objects.filter(fornitore=fornitore.pk)
            qs1=Order.objects.filter(Q(data_ordine__gte=datainizio)).filter(fornitore=fornitore)
            qs2=Order.objects.filter(Q(data_ordine__lte=datafine)).filter(fornitore=fornitore)
            a=elenco.intersection(qs1,qs2)
            response=HttpResponse('text/csv')
            response['Content-Disposition']='attachment;filename=elencoordini.csv'
            writer=csv.writer(response)
            writer.writerow(['Numero Ordine', 'Fornitore','Data Ordine', 'Prodotto','Imponibile singolo pezzo','Totale imponibile ordine'] )
            ordine=a.values_list('id', 'fornitore__ragioneSociale','data_ordine','prodotto','prezzo_concordato', 'importo_ordine')
            for serv in ordine:
                writer.writerow(serv)
            return response
            
    return render(request, 'contabilità/servizimese.html',{'form':form})

    