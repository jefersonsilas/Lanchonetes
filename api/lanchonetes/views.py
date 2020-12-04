from .models import Loja, Categoria, Produto, Promocao
from .serializers import LojaSerializer, CategoriaSerializer, ProdutoSerializer, PromocaoSerializer
from django.contrib.auth import authenticate, login, logout #importação dos métodos utilizados para ver o login/logout e autenticação
from django.contrib.auth.models import Group, Permission, User
from django.db import IntegrityError
from rest_framework.authentication import BasicAuthentication
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404

class Login(APIView):

    def post(self, request):
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['senha']
        try:
            user = User.objects.create_user(nome, email, senha)
            user.save()
            if user is not None:
                cliente = Group.objects.get(name='cliente')
                user.groups.add(cliente)
                login(request,user)
                return Response(True, status=status.HTTP_200_OK)
        except (Exception, IntegrityError) as e:
            return Response(data=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def get(self, request):
        nome = request.POST['nome']
        senha = request.POST['senha']
        user = authenticate(request, username=nome, password=senha) #método para verificar se a senha está correta
        if user is not None:
            login(request, user)
            return Response(True, status=status.HTTP_200_OK)
        else:
            return Response(False, status=status.HTTP_401_UNAUTHORIZED)


class Logout(APIView):

    def get(self, request):
        logout(request)
        return Response(True)
        

class LojasList(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_user_permissions(self, user):
        if user.is_superuser:
            return Permission.objects.all()
        return user.user_permissions.all() | Permission.objects.filter(group__user=user)
    def get(self, request, format=None):
        
        print(self.get_user_permissions(user=request.user))
        if not request.user.has_perm('lanchonetes.view_loja'):
            return Response(False, status=status.HTTP_401_UNAUTHORIZED)

        get_data = request.query_params
        lojas = Loja.objects.all()     
        serializer = LojaSerializer(lojas, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        print(self.get_user_permissions(user=request.user))
        if not request.user.has_perm('lanchonetes.add_loja'):
            return Response(False, status=status.HTTP_401_UNAUTHORIZED)
        serializer = LojaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LojaDetail(APIView):    
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Loja.objects.get(pk=pk)
        except Loja.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        if not request.user.has_perm('lanchonetes.view_loja'):
            return Response(False, status=status.HTTP_401_UNAUTHORIZED)
        loja = self.get_object(pk)
        serializer = LojaSerializer(loja)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        if not request.user.has_perm('lanchonetes.change_loja'):
            return Response(False, status=status.HTTP_401_UNAUTHORIZED)
        loja = self.get_object(pk)
        serializer = LojaSerializer(loja, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        if not request.user.has_perm('lanchonetes.change_loja'):
            return Response(False, status=status.HTTP_401_UNAUTHORIZED)
        loja = self.get_object(pk)
        serializer = LojaSerializer(loja, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        if not request.user.has_perm('lanchonetes.delete_loja'):
            return Response(False, status=status.HTTP_401_UNAUTHORIZED)
        loja = self.get_object(pk)
        loja.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProdutosList(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        if not request.user.has_perm('lanchonetes.view_produto'):
            return Response(False, status=status.HTTP_401_UNAUTHORIZED)
        authentication_classes = [BasicAuthentication]
        permission_classes = [IsAuthenticated]
        get_data = request.query_params
        produtos = Produto.objects.all()
        if 'categoria' in get_data:
            produtos = produtos.filter(categoria=get_data.get('categoria'))        
        serializer = ProdutoSerializer(produtos, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        if not request.user.has_perm('lanchonetes.add_produto'):
            return Response(False, status=status.HTTP_401_UNAUTHORIZED)
        authentication_classes = [BasicAuthentication]
        permission_classes = [IsAuthenticated]
        serializer = ProdutoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProdutoDetail(APIView):   
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated] 

    def get_object(self, pk):
        try:
            return Produto.objects.get(pk=pk)
        except Produto.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        if not request.user.has_perm('lanchonetes.view_produto'):
            return Response(False, status=status.HTTP_401_UNAUTHORIZED)
        produto = self.get_object(pk)
        serializer = ProdutoSerializer(produto)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        if not request.user.has_perm('lanchonetes.change_produto'):
            return Response(False, status=status.HTTP_401_UNAUTHORIZED)
        produto = self.get_object(pk)
        serializer = ProdutoSerializer(produto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        if not request.user.has_perm('lanchonetes.change_produto'):
            return Response(False, status=status.HTTP_401_UNAUTHORIZED)
        produto = self.get_object(pk)
        serializer = ProdutoSerializer(produto, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        if not request.user.has_perm('lanchonetes.delete_produto'):
            return Response(False, status=status.HTTP_401_UNAUTHORIZED)
        produto = self.get_object(pk)
        produto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PromocoesList(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        if not request.user.has_perm('lanchonetes.view_promocao'):
            return Response(False, status=status.HTTP_401_UNAUTHORIZED)
        promocoes = Promocao.objects.all()
        serializer = PromocaoSerializer(promocoes, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        if not request.user.has_perm('lanchonetes.add_promocao'):
            return Response(False, status=status.HTTP_401_UNAUTHORIZED)
        serializer = PromocaoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PromocaoDetail(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Promocao.objects.get(pk=pk)
        except Promocao.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        if not request.user.has_perm('lanchonetes.view_promocao'):
            return Response(False, status=status.HTTP_401_UNAUTHORIZED)
        promocao = self.get_object(pk=pk)
        serializer = PromocaoSerializer(promocao)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        if not request.user.has_perm('lanchonetes.change_promocao'):
            return Response(False, status=status.HTTP_401_UNAUTHORIZED)
        promocao = self.get_object(pk=pk)
        serializer = PromocaoSerializer(promocao, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        if not request.user.has_perm('lanchonetes.change_promocao'):
            return Response(False, status=status.HTTP_401_UNAUTHORIZED)
        promocao = self.get_object(pk=pk)
        serializer = PromocaoSerializer(promocao, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        if not request.user.has_perm('lanchonetes.delete_promocao'):
            return Response(False, status=status.HTTP_401_UNAUTHORIZED)
        produto = self.get_object(pk=pk)
        produto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)