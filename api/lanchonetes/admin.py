from django.contrib import admin
from .models import Loja, Produto, Promocao, Categoria

class LojaAdmin(admin.ModelAdmin):
    list_display = ("nome","cidade","uf","email")

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("nome", "imagem", "descricao", "categoria")

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome",)

class PromocaoAdmin(admin.ModelAdmin):
    list_display = ("produto","loja","preco","cupom","destaque")

admin.site.register(Loja, LojaAdmin)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Promocao, PromocaoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
