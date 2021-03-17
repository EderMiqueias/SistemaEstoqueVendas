from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, permission_required

from .models import Produto, Imagem
from .forms import ProdutoModelForm, VendaModelForm, BuscarModelForm, ImagemModelForm
from .views_func import add_estado, gerar_grafico_mensal, gerar_grafico_anual

from operator import attrgetter
from threading import Thread


def logar_usuario(request):
    erro = False
    if str(request.method) == 'POST':
        username = request.POST['username']
        pwd = request.POST['pwd']
        user = authenticate(request, username=username, password=pwd)
        if user is not None:
            login(request, user)
            return redirect('index')
        erro = True
    context = {"erro": erro}
    return render(request, "login.html", context)


@login_required(login_url='/login')
def deslogar_usuario(request):
    logout(request)
    return redirect("login")


@login_required(login_url='/login')
def index(request):
    user_creator = request.user
    t_mes = Thread(gerar_grafico_mensal(user_creator))
    t_ano = Thread(gerar_grafico_anual(user_creator))
    t_mes.start()
    t_ano.start()
    context = {
        'user': user_creator
    }
    return render(request, "index.html", context)


@login_required(login_url='/login')
def vender(request):
    formvenda = VendaModelForm(request.user, request.POST or None)
    if str(request.method) == "POST":
        if formvenda.is_valid():
            formvenda.registrar(request.user)
            formvenda = VendaModelForm(request.user)
            messages.success(request, "Venda Realizada com Sucesso")

        else:
            messages.error(request, "Venda Não Realizada")
    context = {
        'form': formvenda
    }
    return render(request, "vender.html", context)


@permission_required('', login_url='/admin/login/?next=/cadastrar/')
def cadastrar(request):
    formproduto = ProdutoModelForm(request.POST or None)
    formimagem = ImagemModelForm(request.FILES or None)

    if str(request.method) == "POST":
        if formproduto.is_valid():
            pk = formproduto.registrar(request.user)
            formproduto = ProdutoModelForm()

            messages.success(request, "Produto cadastrado com sucesso!")

            if formimagem.is_valid():
                imagem = Imagem(imagem=request.FILES['imagem'])
                imagem.titulo = "p_" + str(pk)
                imagem.salvar()
                formimagem = ImagemModelForm()
        else:
            messages.error(request, "Produto não pode ser cadastrado.")
    context = {
        'form': formproduto,
        'formimagem': formimagem,
        'user_id': request.user.id
    }
    return render(request, "cadastrar.html", context)


@login_required(login_url='/login')
def listar(request):
    user_creator = request.user
    produtos = list(map(add_estado, Produto.objects.filter(user=user_creator)))
    produtos.sort(key=attrgetter('nome'))
    context = {
        'produtos': produtos
    }
    return render(request, "listar.html", context)


@login_required(login_url='/login')
def buscar(request):
    user_creator = request.user
    formbusca = BuscarModelForm(request.POST or None)
    produtos = None
    if str(request.method) == "POST":
        if formbusca.is_valid():
            produtos = formbusca.get_produtos(user_creator)
            if produtos:
                formbusca = BuscarModelForm()
                produtos = list(map(add_estado, produtos))
                produtos.sort(key=attrgetter('nome'))
            else:
                messages.error(request, "Produto Não Encontrado")
    context = {
        'form': formbusca,
        'produtos': produtos
    }
    return render(request, "buscar.html", context)


@permission_required('', login_url='/admin/login/?next=/editar/')
def editar(request, pk):
    produto = Produto.objects.get(id=pk)

    data = produto.to_json()

    formproduto = ProdutoModelForm(data or None)
    formimagem = ImagemModelForm(request.FILES or None)

    if str(request.method) == "POST":
        if formproduto.is_valid() and len(request.POST) == 7:
            produto.nome = request.POST["nome"]
            produto.preco = request.POST["preco"]
            produto.quant = request.POST["quant"]
            produto.quant_minima = request.POST["quant_minima"]

            produto.save()
            formproduto = ProdutoModelForm(data)
            messages.success(request, "Alterações Salvas")

        if formimagem.is_valid():
            imagem = Imagem(imagem=request.FILES['imagem'])
            imagem.titulo = "p_" + str(pk)
            imagem.salvar()
            formimagem = ImagemModelForm()
    context = {
        'formproduto': formproduto,
        'formimagem': formimagem,
        'produto': produto,
    }
    return render(request, "editar.html", context)


@permission_required('', login_url='/admin/login/?next=/deletar/')
def deletar(request, pk):
    Produto.objects.filter(id=pk).delete()
    imagem = Imagem()
    imagem.titulo = pk
    try:
        imagem.remover()
    except FileNotFoundError:
        pass
    messages.info(request, "Produto Excluido")
    return redirect('listar')
