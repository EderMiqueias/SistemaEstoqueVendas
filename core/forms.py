from django import forms
from .models import Produto, Venda
from sistema.db import getdb


class ModeloCharField(forms.CharField):
    def __init__(self, name, ml):
        super().__init__(max_length=ml, label='', widget=forms.TextInput(
            attrs={'placeholder': f'{name}', 'style': 'margin: 1% 0'}
        ))


class ModeloIntegerField(forms.IntegerField):
    def __init__(self, name, required=True):
        super().__init__(label='', required=required, widget=forms.TextInput(
            attrs={'placeholder': f'{name}', 'style': 'margin: 1% 0'}
        ))


class ModeloDecimalField(forms.DecimalField):
    def __init__(self, name, required=True):
        super().__init__(label='', required=required, widget=forms.TextInput(
            attrs={'placeholder': f'{name}', 'style': 'margin: 1% 0'}
        ))


class ImagemModelForm(forms.Form):
    imagem = forms.ImageField(
        label='Select a Image',
        help_text='max. 42 megabytes',
        required=False
    )


class ProdutoModelForm(forms.Form):
    nome = ModeloCharField('Nome', 50)
    preco = ModeloDecimalField('Preço')
    quant = ModeloIntegerField('Quantidade')
    quant_minima = ModeloIntegerField('Quantidade Minima')
    db = getdb()

    def salvar(self):
        produto = Produto(
            nome=self.cleaned_data['nome'],
            preco=float(self.cleaned_data['preco']),
            quant=self.cleaned_data['quant'],
            quant_minima=self.cleaned_data['quant_minima']
        )
        self.db.produtos.insert_one(
            produto.to_json()
        )
    def checagem(self):
        return checar_produto(self.cleaned_data['nome'])


def get_produto_json(nome_produto):
    collect = getdb()['produtos']
    produto = collect.find_one({"nome": nome_produto})
    return produto


def checar_produto(nome_produto, quant=-1):
    produto = get_produto_json(nome_produto)
    if nome_produto == 'default':
        return 500
    if produto:
        produto = Produto.from_json(produto)
        if int(produto.quant) >= quant:
            return 200
        else:
            return 500
    return 404


class VenderModelForm(forms.Form):
    nome_produto = ModeloCharField('Nome do Produto', 40)
    quant = ModeloIntegerField('Quantidade')
    desconto = ModeloDecimalField('Desconto em Reais', required=False)
    db = getdb()
    def registrar(self):
        produto_json = get_produto_json(self.cleaned_data['nome_produto'])
        quant = self.cleaned_data['quant']
        desconto = float(self.cleaned_data['desconto'] or 0)
        valor = (produto_json['preco'] * quant) - desconto
        venda = Venda(
            nome_produto=produto_json['nome'],
            valor=valor,
            quant=quant,
            desconto=desconto
        )
        produto_json['quant'] = int(produto_json['quant']) - venda.quant
        self.db.vendas.insert_one(
            venda.to_json()
        )
        self.db.produtos.update_one(
                {'nome': produto_json['nome']}, {"$set": produto_json}
            )
    def checagem(self):
        return checar_produto(self.cleaned_data['nome_produto'], int(self.cleaned_data['quant']))


class BuscarModelForm(forms.Form):
    nome = ModeloCharField('Nome do Produto', 40)
    def get_produto(self):
        return Produto.from_json(get_produto_json(self.cleaned_data['nome']))
    def checagem(self):
        return checar_produto(self.cleaned_data['nome'])
