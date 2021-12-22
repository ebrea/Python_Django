from django.shortcuts import render, redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime, timedelta
from django.http.response import Http404, JsonResponse


# Create your views here.

# def direciona(req):
#     return redirect('/agenda/')      # função para redirecionar a url (evitando erro)

def logar(request):
     return render(request, 'login.html')

def deslogar(request):
    logout(request)
    return redirect('/')


def autorizacao(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/')            # volta para a página principal
        else:
            messages.error(request, 'Usuário ou senha inválido')
    return redirect('/')                       # volta para a página principal



@login_required(login_url='/login/')    # exige fazer o login antes
def lista_eventos(req):
    usuario = req.user
    data_atual = datetime.now() - timedelta(hours=1)
    evento = Evento.objects.filter(usuario=usuario) #,     # get(id=2)  mostra apenas o item 2
                                    # data_evento__gt=data_atual )      # __gt = great than
    dados = {'eventos':evento}
    return render(req, 'agenda.html', dados)


@login_required(login_url='/login/')    # exige fazer o login antes
def evento(req):
    registro = req.GET.get('id')
    dados = {}
    if registro:
        dados ['evento'] = Evento.objects.get(id=registro)
    return render (req, 'evento.html', dados)


@login_required(login_url='/login/')    # exige fazer o login antes
def submeter_evento(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        usuario = request.user
        registro = request.POST.get('registro')
        if registro:
            evento = Evento.objects.get(id=registro)
            if evento.usuario == usuario:
                evento.titulo = titulo
                evento.descricao = descricao
                evento.data_evento = data_evento
                evento.save()
            # Evento.objects.filter(id=registro).update(titulo=titulo, data_evento=data_evento,
            #                                           descricao=descricao)     # outra forma
        else:
            Evento.objects.create(titulo=titulo, data_evento=data_evento,
                                  descricao=descricao, usuario=usuario)
    return redirect('/')

@login_required(login_url='/login/')    # exige fazer o login antes
def deletar(request, registro):
    usuario = request.user
    try:
        evento = Evento.objects.get(id=registro)
    except Exception:
        raise Http404
    if usuario == evento.usuario:
        evento.delete()
    else:
        raise Http404
    return redirect('/')

@login_required(login_url='/login/')    # exige fazer o login antes
def json_eventos(req):
    usuario = req.user
    evento = Evento.objects.filter(usuario=usuario).values('id','titulo')
    return JsonResponse(list(evento), safe=False)   # usa-se o "safe" por ser lista



