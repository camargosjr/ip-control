from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from .models import MacAddress
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants
from django.contrib import auth
from django.contrib.auth import logout
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator
from datetime import datetime
from django.utils import timezone, dateformat
import re
import logging

# Create your views here.
# senha marina mari@123

regex_mac_adress = "^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})|\
    ([0-9a-fA-F]{4}\\.[0-9a-fA-F]{4}\\.[0-9a-fA-F]{4})$"

def login(request):

    if request.user.is_authenticated:
        return redirect(reverse("mac-control"))

    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username)

        user = auth.authenticate(username=username, password=password)

        if not user:
            messages.add_message(request, constants.ERROR, "Usuário ou senha inválidos.")
            return redirect(reverse("login"))
        
        auth.login(request, user)

        return redirect(reverse("mac-control"))

@login_required
def user_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect(reverse("login"))
    
    raise Http404("Página não encontrada")

def is_registered(request):
    logger = logging.getLogger('djangojr')
   
    today = timezone.now()
    macaddress = request.GET.get('macaddress')
    store = request.GET.get('store')
    
    
    if not macaddress:
        logger.warning('MACADDRESS NAO INFORMADO')
        return HttpResponse("NOT!")
    
    # Verifica se está no formato do endereço mac
    if not re.match(regex_mac_adress,macaddress):
        logger.warning(f'LOJA:{store} MACADDRESS {macaddress} INVALIDO')
        return HttpResponse("NOT!")
    
    
    mac_address = MacAddress.objects.filter(mac_address = macaddress, allowed_days__gte =today )

    # Se macaddress cadastrado retorna "OK!"
    if mac_address:
        logger.info(f"LOJA:{store} {macaddress} AUTORIZADO")
        return HttpResponse("OK!")
    else:
        logger.warning(f'LOJA:{store} {macaddress} NAO CADASTRADO')
        return HttpResponse("NOT!")


@login_required
def mac_control(request):
   
    today = timezone.now()
  
    mac_address_list = MacAddress.objects.filter(allowed_days__gte = today).order_by("-created_at")
    # mac_address_delete = MacAddress.objects.filter(allowed_days__lt = today) 

    # Filtro
    filter_search = request.GET.get('name')
    
    if filter_search:
        filter_search = filter_search.upper()
        mac_address_list = mac_address_list.filter\
            (Q(name__icontains=filter_search) | Q(mac_address__icontains = filter_search))
    
    mac_address_list_pages = Paginator(mac_address_list, 10)
    page_num = request.GET.get('page')
    page_obj = mac_address_list_pages.get_page(page_num)
    proximo = "enable" if page_obj.has_next else "disabled"
    length = len(mac_address_list)
    return render(request, "mac_list.html", {'page_obj': page_obj, 'proximo':proximo})




@login_required
def new_mac(request):
    today = timezone.now()
    if request.method == "GET":
        return render(request, "new_mac.html")
    elif request.method == "POST":
        name = request.POST.get('name').upper()
        mac_address = request.POST.get('mac_address').upper()
        num_days =  request.POST.get('num_days')
        
        # Validações
        if MacAddress.objects.filter(mac_address = mac_address, allowed_days__gte =today).exists():
            messages.add_message(request, constants.WARNING, f"Endereço MAC {mac_address} já cadastrado.")
            return redirect(reverse("new_mac"))
        
        if not name or not mac_address or not num_days:
            messages.add_message(request, constants.WARNING, "Existe campos vazios no formulário.")
            return redirect(reverse("new_mac"))
        

        if not num_days.isdigit():
            messages.add_message(request, constants.WARNING, "Campo 'Tempo' em formato errado!!!")
            return redirect(reverse("new_mac"))
        
        # Checa o formato mac address
        if not re.match(regex_mac_adress,mac_address):
            messages.add_message(request, constants.WARNING,f"Endereço MAC {mac_address} inválido!")
            return redirect(reverse("new_mac"))
        
        days = timezone.timedelta(days=int(num_days))
        
        days_expired = timezone.make_aware(datetime.now() + days)
        # Adiciona 10 anos
        never = timezone.make_aware(datetime.now() + timezone.timedelta(days=3600))
       
        
        new_mac_address = MacAddress(
            name = name,
            mac_address = mac_address,
            authorized = request.user,
            allowed_days = never if int(num_days) == 0 else days_expired
        )

        new_mac_address.save()
        return redirect(reverse("mac-control"))


def delete_mac(request,id_mac):
    mac_address = MacAddress.objects.get(id=id_mac)
    
    mac = mac_address.mac_address
    mac_address.delete()
    messages.add_message(request, constants.SUCCESS,f"Endereço {mac} exluído com Sucesso!")

    return redirect(reverse("mac-control"))