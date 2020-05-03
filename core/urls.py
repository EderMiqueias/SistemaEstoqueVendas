from django.urls import path
from .views import (index, cadastrar, buscar, editar, vender, listar, deletar)

urlpatterns = [
    path("", index, name="index"),
    path("vender/", vender, name="vender"),
    path("cadastrar/", cadastrar, name="cadastrar"),
    path("buscar/", buscar, name="buscar"),
    path("editar/", editar, name="editar"),
    path("listar/", listar, name="listar"),
    path("deletar/<str:pk>", deletar, name="deletar")
]
