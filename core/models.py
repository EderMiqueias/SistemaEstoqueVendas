from django.db import models

from PIL import Image
import shutil
import os
import platform

SO = platform.system()


class Base(models.Model):
    criado = models.DateField('Criação', auto_now_add=True)
    modificado = models.DateField('Atualização', auto_now=True)
    ativo = models.BooleanField("Ativo?", default=True)

    class Meta:
        abstract = True


class Imagem(models.Model):
    imagem = models.ImageField()
    titulo = None

    src_root = 'media/images/' if SO == "Linux" else "media\\images\\"

    def salvar(self):
        img = Image.open(self.imagem)
        img.save(f'{self.src_root}{self.titulo}.png', 'PNG')

    def renomear(self, novo):
        try:
            shutil.move(
                f'{self.src_root}{self.titulo}.png',
                f'{self.src_root}{novo}.png'
            )
        except FileNotFoundError:
            # nao possui imagem
            pass

    def remover(self):
        os.remove(f'{self.src_root}{self.titulo}.png')


class Produto(Base):
    nome = models.CharField('Nome', max_length=50)
    preco = models.FloatField('Preço')
    quant = models.IntegerField("Quantidade")
    quant_minima = models.IntegerField("Quantidade Minima")
    imagem = None

    def __str__(self):
        return f"{self.nome} | R$ {self.preco:.2f} | {self.quant} Em Estoque"

    def load_image(self):
        try:
            src = f'images/{self.nome}.png'
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
            'nome': self.nome,
            'preco': self.preco,
            'quant': self.quant,
            'quant_minima': self.quant_minima,
            'criado': self.criado,
            'modificado': self.modificado,
            'ativo': self.ativo
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
            'valor': self.valor,
            'nome_produto': self.produto_id,
            'quant': self.quant,
            'desconto': self.desconto,
            'criado': self.criado,
            'modificado': self.modificado,
            'ativo': self.ativo
        }
