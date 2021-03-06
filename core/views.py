from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Produto, Imagem
from .forms import ProdutoModelForm, VenderModelForm, BuscarModelForm, getdb, ImagemModelForm
from .views_func import add_estado, gerar_grafico_mensal, gerar_grafico_anual
from operator import attrgetter


def index(request):
    return render(request, "index.html")


def vender(request):
    formvenda = VenderModelForm(request.POST or None)
    if str(request.method) == "POST":
        if formvenda.is_valid():
            if formvenda.checagem() == 200:
                formvenda.registrar()
                formvenda = VenderModelForm()
                messages.success(request, "Venda Realizada com Sucesso")
                gerar_grafico_mensal()
                gerar_grafico_anual()
            elif formvenda.checagem() == 404:
                messages.error(request, "Venda Não Realizada, Produto não Encontrado")
            elif formvenda.checagem() == 500:
                messages.error(request, "Venda Não Realizada, Quantidade Insuficiente para este Produto")
    context = {
        'form': formvenda
    }
    return render(request, "vender.html", context)


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
            if formproduto.checagem() == 404:
                formproduto.salvar()
                formproduto = ProdutoModelForm()
                messages.success(request, "Produto cadastrado com Sucesso")
            else:
                messages.error(request, "Produto de Mesmo Nome já registrado")
    context = {
        'form': formproduto,
        'formimagem': formimagem
    }
    return render(request, "cadastrar.html", context)


def buscar(request):
    formbusca = BuscarModelForm(request.POST or None)
    produto = None
    if str(request.method) == "POST":
        if formbusca.is_valid():
            if formbusca.checagem() != 404:
                produto = formbusca.get_produto()
                formbusca = BuscarModelForm()
            else:
                messages.error(request, "Produto Não Encontrado")
    context = {
        'form': formbusca,
        'produto': produto
    }
    return render(request, "buscar.html", context)


def editar(request):
    formbusca = BuscarModelForm(request.POST or None)
    formproduto = ProdutoModelForm(request.POST or None)
    formimagem = ImagemModelForm(request.FILES or None)
    nome = None
    found = False
    if str(request.method) == "POST":
        if len(request.POST) == 2:
            if formbusca.is_valid():
                if formbusca.checagem() != 404:
                    produto = formbusca.get_produto()
                    formproduto = ProdutoModelForm(produto.to_json())
                    formbusca = BuscarModelForm()
                    nome = produto.nome
                    found = True
                else:
                    messages.error(request, "Produto Não Encontrado")
        else:
            if formproduto.is_valid():
                old_name = request.POST['old_name']
                produto = Produto.from_json(request.POST)
                formproduto = ProdutoModelForm(produto.to_json())
                db = getdb()
                db.produtos.update_one(
                    {'nome': old_name}, {"$set": produto.to_json()}
                )
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


def listar(request):
    db = getdb()
    importacoes = db.produtos.find()
    produtos = list()
    for mapa in importacoes:
        produtos.append(Produto.from_json(mapa))
    produtos = list(map(add_estado, produtos))
    produtos.sort(key=attrgetter('nome'))
    context = {
        'produtos': produtos
    }
    return render(request, "listar.html", context)


def deletar(request, pk):
    db = getdb()
    db.produtos.delete_one({'nome': pk})
    imagem = Imagem()
    imagem.titulo = pk
    try:
        imagem.remover()
    except FileNotFoundError:
        pass
    messages.info(request, "Produto Excluido")
    return redirect('editar')
