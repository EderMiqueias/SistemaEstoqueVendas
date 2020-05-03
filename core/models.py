from datetime import datetime
from django.db import models
from PIL import Image
import shutil
import os


class Imagem(models.Model):
    imagem = models.ImageField()
    titulo = None
    # for linux
    src_root = 'media/images/'

    def salvar(self):
        img = Image.open(self.imagem)
        img.save(f'{self.src_root}{self.titulo}.png', 'PNG')

    def renomear(self, novo):
        shutil.move(
            f'{self.src_root}{self.titulo}.png',
            f'{self.src_root}{novo}.png'
        )

    def remover(self):
        os.remove(f'{self.src_root}{self.titulo}.png')


class Produto:
    nome = None
    preco = None
    quant = None
    quant_minima = None
    imagem = None

    def __init__(self, nome=None, preco=None, quant=None, quant_minima=None):
        self.nome = nome
        self.preco = preco
        self.quant = quant
        self.quant_minima = quant_minima
        self.imagem = self.load_image()

    def load_image(self):
        try:
            src = f'images/{self.nome}.png'
            img = Image.open('media/'+src)
            img.src = src
            return img
        except FileNotFoundError:
            src = f'images/default.png'
            img = Image.open('media/'+src)
            img.src = src
            return img

    def to_json(self):
        return {
            'nome': self.nome,
            'preco': float(self.preco),
            'quant': int(self.quant),
            'quant_minima': int(self.quant_minima)
        }

    @staticmethod
    def from_json(data):
        return Produto(
            nome=data['nome'],
            preco=data['preco'],
            quant=data['quant'],
            quant_minima=data['quant_minima']
        )


class Venda:
    nome_produto = None
    quant = None
    desconto = None
    data = None
    valor = None

    def __init__(self, valor=None, nome_produto=None, quant=None, desconto=None, data=None):
        self.valor = valor
        self.nome_produto = nome_produto
        self.quant = quant
        self.desconto = desconto
        if data:
            self.data = data
        else:
            self.data = datetime.now().strftime('%d%m%Y')

    def to_json(self):
        return {
            'valor': self.valor,
            'nome_produto': self.nome_produto,
            'quant': self.quant,
            'desconto': self.desconto,
            'data': self.data
        }

    @staticmethod
    def from_json(data):
        return Venda(
            valor=data['valor'],
            nome_produto=data['nome_produto'],
            desconto=data['desconto'],
            quant=data['quant'],
            data=data['data']
        )
