from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def index(request):
	return render(request, 'index.html')

def autocadastro(request):
    pass

@login_required
def pagina_de_listagem(request):
    pass

@login_required
def agendamento(request):
    pass

@login_required
def painel_administrativo(request):
    pass