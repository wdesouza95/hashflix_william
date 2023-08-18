from django.shortcuts import render, redirect, reverse
from .models import Filme, Usuario
from .forms import CriarContaForm, FormHomepage
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

# fbv - função para views - uma para cada view - vc precisa definir sobre a maioria das coisas
# cbv - classe para views - uma para cada view - o django vai denifir mt coisa, se usar a class correta

# def homepage(request):
#     return render(request, "homepage.html")


class Homepage(FormView):
    template_name = "homepage.html"
    form_class = FormHomepage

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('filme:homefilmes')  # redireciona para homefilmes
        else:
            return super().get(request, *args, **kwargs) # redireciona para homepage

    def get_success_url(self): #oq fazer se o formulario der certo, reverse quando pede um texto de link(http://...)
        email = self.request.POST['email']
        usuarios = Usuario.objects.filter(email=email)
        if usuarios:
            return reverse('filme:login')
        else:
            return reverse('filme:criarconta')

# fbv: url - view - html
# def homefilmes(request):
#     context = {}
#     lista_filmes = Filme.objects.all()
#     context['lista_filmes'] = lista_filmes
#     return render(request, "homefilmes.html", context)

class Homefilmes(LoginRequiredMixin, ListView):
    template_name = "homefilmes.html"
    model = Filme
    # object_list

class Detalhesfilme(LoginRequiredMixin, DetailView):
    template_name = "detalhesfilme.html"
    model = Filme
    # object -> 1 item da lista por link

    def get(self, request, *args, **kwargs):
        # qual filme ele ta acessando, e depois somar a visualização
        filme = self.get_object()
        filme.visualizacoes += 1
        #salvar banco de dados
        filme.save()
        usuario = request.user
        usuario.filmes_vistos.add(filme)
        return super().get(request, *args, **kwargs) #redireciona para url final

    def get_context_data(self, **kwargs):
        context = super(Detalhesfilme, self).get_context_data(**kwargs)
        filmes_relacionados = Filme.objects.filter(categoria=self.get_object().categoria)[0:5]
        context['filmes_relacionados'] = filmes_relacionados
        return context


class Pesquisafilme(LoginRequiredMixin, ListView):
    template_name = "pesquisa.html"
    model = Filme

    #editando o object list
    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('query') #nome do parametro definido no html
        if termo_pesquisa:
            object_list = self.model.objects.filter(titulo__icontains=termo_pesquisa) #se o Titulo contém
            return object_list
        else:
            return None

class Paginaperfil(LoginRequiredMixin, UpdateView):
    template_name = "editarperfil.html"
    model = Usuario
    fields = ['first_name', 'last_name', 'email']

    def get_success_url(self):
        return reverse('filme:homefilmes')

class Criarconta(FormView):
    template_name = "criarconta.html"
    form_class = CriarContaForm

    def form_valid(self, form): #quando cria no banco de dados
        form.save()
        return super().form_valid(form)

    def get_success_url(self): #oq fazer se o formulario der certo, reverse quando pede um texto de link(http://...)
        return reverse('filme:login')

