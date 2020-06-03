# SistemaEstoqueVendas

Sistema de cadastro e vendas usando [django](https://www.djangoproject.com/), [MongoDB](https://www.mongodb.com/), [Bootstrap4](https://getbootstrap.com/) e [Matplotlib](https://matplotlib.org/)

# Linux
### Instalação

```shell
pip install --upgrade pip setuptools
pip install -r requirements.txt
```

### Execução

```shel
gunicorn --bind 127.0.0.1:8000 sistema.wsgi
```

# Windows
### Instalação

```shel
pip install --upgrade pip setuptools
pip install -r requirements.txt
pip install waitress
```

### Execução

```shel
# O gunicorn é exclusivo para Unix, sendo assim, você pode usar o Waitress como substituto
waitress-serve --listen=*:8000 sistema.wsgi:application
```
