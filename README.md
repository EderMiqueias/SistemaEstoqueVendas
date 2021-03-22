# SistemaEstoqueVendas

Sistema de cadastro e vendas usando [django](https://www.djangoproject.com/), [SQLite3](https://www.sqlite.org/index.html), [Bootstrap4](https://getbootstrap.com/) e [Matplotlib](https://matplotlib.org/)

# Linux
### Instalação

```shell
pip install --upgrade pip setuptools
pip install -r requirements.txt
```

### Migração

```shel
python manage.py migrate
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

### Migração

```shel
python manage.py migrate
```

### Execução

```shel
# O gunicorn é exclusivo para Unix, sendo assim, você pode usar o Waitress como substituto
waitress-serve --listen=*:8000 sistema.wsgi:application
```
