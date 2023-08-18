# esse arquivo é um gerenciador de context: variavéis personalizaveis, além daquelas q o django já tem pronta
# cada nova varaivel precisa ser adicionada no nosso settings.py, nos templates

from .models import Filme

def lista_filmes_recentes(request):
    lista_filmes = Filme.objects.all().order_by('-data_criacao')[0:8] #menos na frente ordena em ordem descrecente
    if lista_filmes:
        filme_destaque = lista_filmes[0]
    else:
        filme_destaque = None
    return {"lista_filmes_recentes": lista_filmes, "filme_destaque": filme_destaque}


def lista_filmes_emalta(request):
    lista_filmes = Filme.objects.all().order_by('-visualizacoes')[0:8]
    return {"lista_filmes_emalta": lista_filmes}
