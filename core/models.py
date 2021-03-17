from django.db import models
from django.conf import settings

from PIL import Image
import shutil
import os
import platform

SO = platform.system()


class Base(models.Model):
    criado = models.DateField('Criação', auto_now_add=True)
    modificado = models.DateField('Atualização', auto_now=True)
    ativo = models.BooleanField("Ativo?", default=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Imagem(models.Model):
    imagem = models.ImageField()
    titulo = None

    src_root = 'media/images/' if SO == "Linux" else "media\\images\\"

    def salvar(self):
        img = Image.open(self.imagem)
        img.save(f'{self.src_root}{self.titulo}.png', 'PNG')

    def remover(self):
        os.remove(f'{self.src_root}{self.titulo}.png')


class Produto(Base):
    nome = models.CharField('Nome', max_length=50)
    preco = models.FloatField('Preço')
    quant = models.IntegerField("Quantidade")
    quant_minima = models.IntegerField("Quantidade Minima")
    imagem = None

    def __str__(self):
        return f"{self.nome} | R$ {self.preco} | {self.quant} Em Estoque"

    def load_image(self):
        try:
            src = f'images/p_{self.id}.png'
            img = Image.open('media/'+src)
            img.src = src
            self.imagem = img
        except FileNotFoundError:
            src = f'images/default.png'
            img = Image.open('media/'+src)
            img.src = src
            self.imagem = img

    def to_json(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'preco': self.preco,
            'quant': self.quant,
            'quant_minima': self.quant_minima,
            'criado': self.criado,
            'modificado': self.modificado,
            'ativo': self.ativo,
            'user_id': str(self.user.id)
        }


class Venda(Base):
    produto_id = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quant = models.IntegerField('Quantidade')
    desconto = models.FloatField('Desconto')

    def __str__(self):
        return f"{self.produto_id} | {self.valor} | {self.quant}"

    @property
    def valor(self):
        return (self.produto_id.preco * self.quant) - self.desconto

    def to_json(self):
        return {
            'id': self.id,
            'valor': self.valor,
            'nome_produto': self.produto_id,
            'quant': self.quant,
            'desconto': self.desconto,
            'criado': self.criado,
            'modificado': self.modificado,
            'ativo': self.ativo,
            'user_id': str(self.user.id)
        }
