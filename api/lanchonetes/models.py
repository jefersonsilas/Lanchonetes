from django.db import models
from django.utils import timezone

class Loja(models.Model):
    nome = models.CharField(max_length=200)
    cidade = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)
    email = models.EmailField()
    
    class Meta:
        verbose_name = ("Loja")
        verbose_name_plural = ("Lojas")
    
    def __str__(self):
        return self.nome

class Categoria(models.Model):

    nome = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = ("Categoria")
        verbose_name_plural = ("Categorias")
    
    def __str__(self):
        return self.nome

class Produto(models.Model):

    nome = models.CharField(max_length=200)
    imagem = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.RESTRICT)

    class Meta:
        verbose_name = ("Produto")
        verbose_name_plural = ("Produtos")
    
    def __str__(self):
        return self.nome


class Promocao(models.Model):

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE)
    preco = models.DecimalField(max_digits=15,decimal_places=2)
    cupom = models.CharField(max_length=20)
    destaque = models.BooleanField(default=False)

    
    class Meta:
        verbose_name = ("Promoção")
        verbose_name_plural = ("Promoções")
    
    def __str__(self):
        return self.cupom


