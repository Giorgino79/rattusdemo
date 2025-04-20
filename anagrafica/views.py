
from django.shortcuts import render, get_object_or_404,redirect
from .models import Azienda, Filiali, Fornitori, Privati
from anagrafica.forms import AziendaForm, FilialiForm, FornitoriForm, PrivatiForm, AggiornaAzienda,AggFornitoriForm, AggiornaFiliale
from django.views.generic import FormView, ListView
from django.http import HttpResponseRedirect
import string
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from logistica.models import Install


class InsAna(PermissionRequiredMixin,FormView):
    permission_required='anagrafica.add_azienda'
    redirect_field_name=('login')
    permission_denied_message=('Non sei autorizzato')
    template_name='anagrafica/nuova-anagrafica.html'
    context_object_name='qs'
    form_class=AziendaForm
    i_instance=None
    
    def get_success_url(self):
        return self.request.path
    
    def get_queryset(self):
        return Azienda.objects.all()
    

    def form_valid(self, form):
        self.i_instance=form.save()
        messages.add_message(self.request, messages.INFO, f'Nuovo cliente numero: {self.i_instance.id} - {self.i_instance.ragioneSociale} è stato creato con successo')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print(form.errors)
        self.object_list = self.get_queryset()
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)

@permission_required({('anagrafica.add_azienda')})
def aggazienda(request,pk):
    azienda=get_object_or_404(Azienda, pk=pk)
    form=AggiornaAzienda(instance=azienda)
    if request.method=='POST':
         form=AggiornaAzienda(request.POST,instance=azienda)
         if form.is_valid():
            form.save()
            return redirect('anagrafica:elencoclienti')
    return render(request, 'anagrafica/aggiornaazienda.html',{'form':form})

def aggfornitore(request,pk):
    azienda=get_object_or_404(Fornitori, pk=pk)
    form=AggFornitoriForm(instance=azienda)
    if request.method=='POST':
         form=AggFornitoriForm(request.POST,instance=azienda)
         if form.is_valid():
            form.save()
            return redirect('anagrafica:elencofornitori')
    return render(request, 'anagrafica/aggiornafornitori.html',{'form':form})
     

class InsFil(FormView, ListView):
    model=Filiali
    template_name='anagrafica/filiali.html'
    context_object_name='qs'
    form_class = FilialiForm
    i_instance=None
    
    def get_success_url(self):
        return self.request.path
  
    def get_queryset(self): 
        return Filiali.objects.all()
    
    
    def form_valid(self, form):
        self.i_instance=form.save()
        messages.add_message(self.request, messages.INFO, f'Nuova Filiale numero: {self.i_instance.nomeFiliale} - {self.i_instance.anaFiliale} è stato creato con successo')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print(form.errors)
        self.object_list = self.get_queryset()
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)
    
def elenco(request):
    clienti=Azienda.objects.all()
    return render(request, 'anagrafica/elencoanagrafica.html',{'clienti':clienti})


def vediana(request, pk):
    clienti=Azienda.objects.get(pk=pk)
    install=Install.objects.filter(azienda__pk=clienti.pk)
    return render(request, 'anagrafica/vedicodice.html', {'c':clienti, 'insta':install})

class InsFor(FormView,ListView):
    template_name='anagrafica/nuovo-fornitore.html'
    context_object_name='qs'
    form_class=FornitoriForm
    i_instance=None
    
    def get_success_url(self):
        return self.request.path 
    
    def get_queryset(self):
        return Fornitori.objects.all()
    

    def form_valid(self, form):
        self.i_instance=form.save()
        messages.add_message(self.request, messages.INFO, f'Nuovo Fornitore numero: {self.i_instance.id} - {self.i_instance.ragioneSociale} è stato creato con successo')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print(form.errors)
        self.object_list = self.get_queryset()
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)
    
def elencofornitori(request):
    fornitori=Fornitori.objects.all()
    return render(request, 'anagrafica/elencofornitori.html',{'clienti':fornitori})


def vedifor(request, pk):
    fornitore=Fornitori.objects.get(pk=pk)
    return render(request, 'anagrafica/vedifornitore.html', {'c':fornitore})

class Inspriv(FormView,ListView):
    template_name='anagrafica/nuovo-privato.html'
    context_object_name='qs'
    form_class=PrivatiForm
    i_instance=None
    
    def get_success_url(self):
        return self.request.path
    
    def get_queryset(self):
        return Privati.objects.all()
    

    def form_valid(self, form):
        self.i_instance=form.save()
        messages.add_message(self.request, messages.INFO, f'Nuovo Privato numero: {self.i_instance.id} - {self.i_instance.nome_cognome} è stato creato con successo')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print(form.errors)
        self.object_list = self.get_queryset()
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)
    
def elencoprivati(request):
    privato=Privati.objects.all()
    return render(request, 'anagrafica/elencoprivati.html',{'clienti':privato})

def elencofiliali(request):
    filiali=Filiali.objects.all()
    return render(request, 'anagrafica/elencofiliali.html', {'filiali':filiali})

def aggiornafiliale(request,pk):
    filiale=get_object_or_404(Filiali,pk=pk)
    if request.method=='POST':
        form=AggiornaFiliale(request.POST, instance=filiale)
        if form.is_valid():
            form.save()
            return redirect('anagrafica:elencofiliali')
    else:
        form=AggiornaFiliale(instance=filiale)
    context={'form':form, 'filiale':filiale}
    return render(request, 'anagrafica/aggiornafiliali.html',context)
    

def vedipriv(request, pk):
    privato=Privati.objects.get(pk=pk)
    install=Install.objects.filter(privato__pk=privato.pk)
    return render(request, 'anagrafica/vediprivato.html', {'c':privato,'insta':install})

def aggprivato(request,pk):
    privato=get_object_or_404(Privati, pk=pk)
    form=PrivatiForm(instance=privato)
    if request.method=='POST':
         form=PrivatiForm(request.POST,instance=privato)
         if form.is_valid():
             form.save()
         return HttpResponseRedirect('anagrafica:elencoclienti')
    return render(request, 'anagrafica/aggiornaprivato.html',{'form':form})
