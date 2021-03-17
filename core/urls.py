from django.urls import path
from .views import (index, cadastrar, buscar, editar, vender, listar, deletar, logar_usuario, deslogar_usuario)

urlpatterns = [
    path("", index, name="index"),
    path("vender/", vender, name="vender"),
    path("cadastrar/", cadastrar, name="cadastrar"),
    path("buscar/", buscar, name="buscar"),
    path("editar/<str:pk>", editar, name="editar"),
    path("listar/", listar, name="listar"),
    path("deletar/<str:pk>", deletar, name="deletar"),
    path("login/", logar_usuario, name="login"),
    path("logout/", deslogar_usuario, name="logout")
]
