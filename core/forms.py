from django import forms
from .models import Produto, Venda


class ModeloCharField(forms.CharField):
    def __init__(self, name="", ml=50, **kwargs):
        super().__init__(**kwargs, max_length=ml, label='', widget=forms.TextInput(
            attrs={'placeholder': f'{name}', 'style': 'margin: 1% 0'}
        ))


class ModeloIntegerField(forms.IntegerField):
    def __init__(self, name="", required=True, **kwargs):
        super().__init__(**kwargs, label='', required=required, widget=forms.TextInput(
            attrs={'placeholder': f'{name}', 'style': 'margin: 1% 0'}
        ))


class ModeloDecimalField(forms.DecimalField):
    def __init__(self, name="", required=True, **kwargs):
        super().__init__(**kwargs, label='', required=required, widget=forms.TextInput(
            attrs={'placeholder': f'{name}', 'style': 'margin: 1% 0'}
        ))


class ImagemModelForm(forms.Form):
    imagem = forms.ImageField(
        label='Select a Image',
        help_text='max. 42 megabytes',
        required=False
    )


def get_produto_json(nome_produto):
    produto = Produto.objects.filter(nome__icontains=nome_produto)
    return produto[0].to_json() if produto else produto


def get_produtos_json(nome_produto):
    produtos = list(filter(lambda x: f"{nome_produto}" in x.to_json()["nome"], list(Produto.objects.all())))
    return produtos


def get_produtos_produto(nome_produto):
    return Produto.objects.filter(nome__icontains=nome_produto)


def checar_produto(nome_produto, quant=-1):
    produto_json = get_produto_json(nome_produto)
    if nome_produto == 'default':
        return 500
    if produto_json:
        if int(produto_json["quant"]) >= quant:
            return 200
        else:
            return 500
    return 404


class ProdutoModelForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'preco', 'quant', 'quant_minima']
        labels = {
            'nome': "",
            'preco': "",
            'quant': "",
            'quant_minima': ""
        }
        help_texts = {
            'nome': "Nome",
            'preco': "Preço",
            'quant': "Quantidade",
            'quant_minima': "Quantidade Mínima"
        }


class VendaModelForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ['produto_id', 'quant', 'desconto']
        labels = {
            'produto_id': "",
            'desconto': "",
            'quant': "",
        }
        help_texts = {
            'produto_id': "Produto",
            'desconto': "Desconto",
            'quant': "Quantidade",
        }


class BuscarModelForm(forms.Form):
    nome = ModeloCharField('Nome do Produto', 50)

    def get_produto_json(self):
        return get_produto_json(self.cleaned_data['nome'])

    def get_produtos(self):
        produtos = get_produtos_produto(self.cleaned_data['nome'])
        return produtos
