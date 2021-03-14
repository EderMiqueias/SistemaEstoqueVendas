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
    t_mes = Thread(gerar_grafico_mensal())
    t_ano = Thread(gerar_grafico_anual())
    t_mes.start()
    t_ano.start()
    return render(request, "index.html")


@login_required(login_url='/login')
def vender(request):
    formvenda = VendaModelForm(request.POST or None)
    if str(request.method) == "POST":
        if formvenda.is_valid():
            formvenda.save()
            formvenda = VendaModelForm()
            messages.success(request, "Venda Realizada com Sucesso")

            # if formvenda.checagem() == 200:
            #     formvenda.registrar()
            #     formvenda = VenderModelForm()
            #     messages.success(request, "Venda Realizada com Sucesso")
            #     gerar_grafico_mensal()
            #     gerar_grafico_anual()
            # elif formvenda.checagem() == 404:
            #     messages.error(request, "Venda Não Realizada, Produto não Encontrado")
            # elif formvenda.checagem() == 500:
            #     messages.error(request, "Venda Não Realizada, Quantidade Insuficiente para este Produto")
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
            if formimagem.is_valid():
                imagem = Imagem(imagem=request.FILES['imagem'])
                imagem.titulo = request.POST['nome']
                imagem.salvar()
                formimagem = ImagemModelForm()
            formproduto.save()
            formproduto = ProdutoModelForm()
            messages.success(request, "Produto cadastrado com sucesso!")
        else:
            messages.error(request, "Produto não pode ser cadastrado.")
    context = {
        'form': formproduto,
        'formimagem': formimagem
    }
    return render(request, "cadastrar.html", context)


@login_required(login_url='/login')
def buscar(request):
    formbusca = BuscarModelForm(request.POST or None)
    produtos = None
    if str(request.method) == "POST":
        if formbusca.is_valid():
            produtos = formbusca.get_produtos()
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
def editar(request):
    formbusca = BuscarModelForm(request.POST or None)
    formproduto = ProdutoModelForm(request.POST or None)
    formimagem = ImagemModelForm(request.FILES or None)
    nome = None
    found = False
    if str(request.method) == "POST":
        if len(request.POST) == 2:
            if formbusca.is_valid():
                if formbusca.get_produtos():
                    produto_json = formbusca.get_produto_json()
                    formproduto = ProdutoModelForm(produto_json)
                    formbusca = BuscarModelForm()
                    nome = produto_json["nome"]
                    found = True
                else:
                    messages.error(request, "Produto Não Encontrado")
        else:
            if formproduto.is_valid():
                old_name = request.POST['old_name']

                formproduto = ProdutoModelForm(request.POST)
                produto = Produto.objects.filter(nome=old_name)
                if produto:
                    produto = produto[0]
                    produto.nome = request.POST["nome"]
                    produto.preco = request.POST["preco"]
                    produto.quant = request.POST["quant"]
                    produto.quant_minima = request.POST["quant_minima"]
                    produto.save()

                messages.success(request, "Alterações Salvas")
                if formimagem.is_valid():
                    imagem = Imagem(imagem=request.FILES['imagem'])
                    imagem.titulo = old_name
                    imagem.salvar()
                    formimagem = ImagemModelForm()
                else:
                    imagem = Imagem()
                    imagem.titulo = old_name
                    if old_name != produto.nome:
                        imagem.renomear(produto.nome)
    context = {
        'formbusca': formbusca,
        'formproduto': formproduto,
        'formimagem': formimagem,
        'nome': nome,
        'found': found
    }
    return render(request, "editar.html", context)


@login_required(login_url='/login')
def listar(request):
    produtos = list(map(add_estado, Produto.objects.all()))
    produtos.sort(key=attrgetter('nome'))
    context = {
        'produtos': produtos
    }
    return render(request, "listar.html", context)


@permission_required('', login_url='/admin/login/?next=/deletar/')
def deletar(request, pk):
    Produto.objects.filter(nome=pk).delete()
    imagem = Imagem()
    imagem.titulo = pk
    try:
        imagem.remover()
    except FileNotFoundError:
        pass
    messages.info(request, "Produto Excluido")
    return redirect('editar')
