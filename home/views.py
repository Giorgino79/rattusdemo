
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from anagrafica.models import Fornitori, Filiali, Privati, Azienda
from servizi.models import Servizio
from logistica.models import Products
from django.http import JsonResponse
from .models import Messaggio
from django.contrib.auth import get_user_model, get_user
from dipendenti.models import Dipendente
from django.views.generic import DeleteView
from dipendenti.models import Giornata
import datetime
from .forms import MessaggioForm


def home(request):
    User=get_user(request)
    
    giornata=Giornata.objects.filter(operatore=User, data=datetime.datetime.now()).exists()
    if giornata:
        Giornata.objects.get(operatore=User,data=datetime.datetime.now())
    else:
        pass
    
    return render(request, 'home/home.html',{ 'giornata':giornata})

def cerca(request):
    if "q" in request.GET:
        querystring = request.GET.get("q")
        if len(querystring) == 0:
            return redirect("/cerca/")
        clienti= Azienda.objects.filter(ragioneSociale__icontains=querystring)
        filiali = Filiali.objects.filter(indFiliale__icontains=querystring)
        fornitori = Fornitori.objects.filter(ragioneSociale__icontains=querystring)
        privati = Privati.objects.filter(nome_cognome__icontains=querystring)
        servizio=Servizio.objects.filter(azienda__ragioneSociale__icontains=querystring)
        serpriv=Servizio.objects.filter(privati__nome_cognome__icontains=querystring)
        prodotti=Products.objects.filter(nome_prodotto__icontains=querystring)
        context = {"clienti": clienti, "filiali": filiali, "serpriv":serpriv,"servizio":servizio,"fornitori": fornitori, 'privati':privati, 'prodotti':prodotti}
        return render(request, 'home/cerca.html', context)
    else:
        return render(request, 'home/cerca.html')



def chat(request):
    user=Dipendente.objects.get(username=request.user)
    form=MessaggioForm(request.POST)
    if request.method=='POST':
        form=MessaggioForm(request.POST)
        if form.is_valid():
            obj=form.save(commit=False)
            destinatario=request.POST['destinatario']
            testo=request.POST['testo']
            dest=Dipendente.objects.get(pk=destinatario)
            messaggio=Messaggio.objects.create(mittente=user,destinatario=dest, testo=testo).save()
           
            return redirect('home:chat')
    else:
        form=MessaggioForm()
    vedi=Messaggio.objects.all().filter(destinatario=user)
    
    return render(request,'home/chat.html', {'form':form, 'vedi':vedi})


class DeleteMessage(DeleteView):
    model=Messaggio
    success_url=reverse_lazy('home:chat')
    template_name='home/cancellamessaggio.html'
    
    def get_queryset(self):
        queryset=super().get_queryset()
        return queryset.filter(destinatario_id=self.request.user.id)