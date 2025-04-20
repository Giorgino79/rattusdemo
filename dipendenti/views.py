from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from .forms import DipendenteForm, Mensilità, InizioGiornata, GiornataForm
from .models import Dipendente, Giornata
from servizi.models import Distinte
from django.db.models import Q
from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from datetime import timedelta, date
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user, get_user_model
from automezzi.models import Automezzo
import logging
logger = logging.getLogger(__name__)


def registradipendente(request):
    form=DipendenteForm(request.POST, request.FILES)
    if request.method=='POST':
        form=DipendenteForm(request.POST, request.FILES)
        if form.is_valid():
            user=form.save()
            messages.success(request,f'Nuovo dipendente con username {user.username} e passord {user.password} creato')
            return redirect('home:home')
    return render(request,'dipendenti/nuovodipendente.html', {'form':form})
            

def elencodipendenti(request):
    dipen=Dipendente.objects.all()
    return render(request, 'dipendenti/elencodipendenti.html',{'dip':dipen})

def vedidipendente(request,pk):
    dipen=Dipendente.objects.get(pk=pk)
    return render(request,'dipendenti/vedidipendente.html', {'dipen':dipen})        

# def entra(request):
#     if request.method=='POST':
#         username=request.POST['username']
#         password=request.POST['password']
#         user=authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request,user)
#             nome=user.username
#             messages.success(request, '<h1>Buongiorno '+nome+'!</h1>')
                
#             return redirect('home:home')
#         else:
#             messages.error(request, 'Non risultano utenti con queste credenziali, controlla di averle digitate bene')
#     return render(request, 'dipendenti/login.html')
        
def entra(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                nome = user.username
                messages.success(request, f'<h1>Buongiorno {nome}!</h1>')
                return redirect('home:home')
            else:
                messages.error(request, 'Non risultano utenti con queste credenziali, controlla di averle digitate bene')
        except Exception as e:
            logger.error(f"Errore durante l'autenticazione dell'utente {username}: {e}", exc_info=True)
            messages.error(request, 'Si è verificato un errore durante il tentativo di accesso. Riprova più tardi.')
            # Potresti scegliere di reindirizzare a una pagina di errore specifica qui
            # return redirect('error_page')
    return render(request, 'dipendenti/login.html')

def aggiornadipendente(request,pk):
    dipen=get_object_or_404(Dipendente,pk=pk)
    form=DipendenteForm(instance=dipen)
    if request.method=='POST':
        form=DipendenteForm(request.POST, request.FILES, instance=dipen)
        if form.is_valid():
            form.save()
            return redirect('dipendenti:elencodipendenti')
    return render(request, 'dipendenti/aggiornadipendente.html',{'form':form,'dipen':dipen})

def esci(request):
    logout(request)
    messages.success(request, 'Buonaserata e grazie per il lavoro svolto')
    return redirect('dipendenti:login')

import datetime
def profilo(request, username):

    user = get_user_model().objects.filter(username=username).first()
    distinta=Distinte.objects.filter(user=user).filter(chiusura=False)
    giornata=Giornata.objects.get(operatore=user, data=datetime.datetime.now())
    oggi=date.today()
    return render(request,"dipendenti/profilo.html",{"user": user, 'distinta':distinta,'giornata':oggi, 'giornata':giornata}  )     


def giornatemesedipendente(request):
    form=Mensilità(request.POST)
    if form.is_valid():
        dipendente=request.POST['dipendente']
        inizio=request.POST.get('data_inizio')
        fine=request.POST.get('data_fine')
        dip=Dipendente.objects.get(pk=dipendente)
        giornata=Giornata.objects.filter(operatore=dip)
        gioin=Giornata.objects.filter(Q(data__gte=inizio)).filter(operatore=dip.pk)
        giofin=Giornata.objects.filter(Q(data__lte=fine)).filter(operatore=dip.pk)
        a=giornata.intersection(gioin,giofin)
        oggi=date.today()
        inizio_settimana=oggi-timedelta(days=oggi.weekday())
        inizio_mese=oggi.replace(day=1)
        
        registrazioni=Giornata.objects.filter(operatore=dip)
        registrazioni_settimana = registrazioni.filter(data__gte=inizio_settimana)
        registrazioni_mese = registrazioni.filter(data__gte=inizio_mese)
        
        def somma_ore(queryset):
            totale = timedelta()
            for entry in queryset:
                ore = entry.daily_hours()
            if ore is not None and isinstance(ore, timedelta):
                totale += ore
            return totale            
        response=BytesIO()
        context={
            'a':a, 
            'dip':dip,
            'inizio':inizio,
            'fine':fine, 
            'giornata':giornata,
            'giornaliere': registrazioni.filter(data=oggi),
            'ore_settimanali': somma_ore(registrazioni_settimana),
            'ore_mensili': somma_ore(registrazioni_mese),
            }
        template_path='dipendenti/oremese.html'
        template=get_template(template_path)
        html=template.render(context)
        response=HttpResponse(content_type='application/pdf')
        response['Content-Disposition']='filename=Giornate'
        pisa_status=pisa.CreatePDF(html, dest=response)
        return response
    return render(request, 'dipendenti/stampamesedipendente.html',{'form':form})
        
    
@login_required
def calcoloore(request):
    oggi=date.today()
    inizio_settimana=oggi-timedelta(days=oggi.weekday())
    inizio_mese=oggi.replace(day=1)
    
    registrazioni=Giornata.objects.filter(operatore=request.user)
    registrazioni_settimana = registrazioni.filter(data__gte=inizio_settimana)
    registrazioni_mese = registrazioni.filter(data__gte=inizio_mese)
    
    def somma_ore(queryset):
        totale = timedelta()
        for entry in queryset:
            ore = entry.daily_hours()
        if ore is not None and isinstance(ore, timedelta):
            totale += ore
        return totale

    context = {
        'giornaliere': registrazioni.filter(data=oggi),
        'oggi':somma_ore(oggi),
        'ore_settimanali': somma_ore(registrazioni_settimana),
        'ore_mensili': somma_ore(registrazioni_mese),
    }

    return render(request, 'dipendenti/ore.html', context)

#giornata___________________
  
def nuovagiornata(request):
    User=get_user(request)
    
    giornata=Giornata.objects.filter(operatore=User, data=datetime.datetime.now()).exists()
    if giornata:
        giorno=Giornata.objects.get(operatore=User,data=datetime.datetime.now())
        return redirect('dipendenti:aggiornagiornata',pk=giorno.pk)
    else:
        form =InizioGiornata(request.POST)
        if request.method=='POST':
            form=InizioGiornata(request.POST)
            if form.is_valid():
                obj=form.save(commit=False)
                mezzo=request.POST.get('mezzo')
                inizio=request.POST['ora_inizio_mattina']
                furgone=Automezzo.objects.get(pk=mezzo)
                nuova=Giornata.objects.create(operatore=User, mezzo=furgone,ora_inizio_mattina=inizio).save()
                form=InizioGiornata()
                return redirect('dipendenti:profilo', username=User)
    return render(request,'dipendenti/iniziogiornata.html',{'form':form})


def aggiornagiornata(request,pk):
    giorno=Giornata.objects.get(pk=pk)
    form=GiornataForm(request.POST, instance=giorno)
    if request.method=='POST':
        form=GiornataForm(request.POST,instance=giorno)
        if form.is_valid():   
            form.save()
            return redirect('dipendenti:profilo', username=giorno.operatore.username) 
    return render(request,'dipendenti/aggiornagiornata.html',{'form':form})
