import json
from django.http import JsonResponse
from django.shortcuts import render
from gestiondata.models import Fournisseur,Menu,Articles,TypeMenu,Url,Categorie
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import FournisseurSerializer, MenuSerializer, ArticlesSerializer, TypeMenuSerializer, UrlSerializer, CategorieSerializer
from rest_framework import status
from rest_framework.decorators import api_view


#----------------------------------Fournisseur----#--------------------------------------
# class based views
# List and Create == GET and POST
class FournisseurListCreateView(APIView):
    def get(self, request):
        format = request.query_params.get('format', 'full')
        fournisseurs = Fournisseur.objects.all()
        if format == 'minimal':
            data = [{'id': f.id, 'name': f.name} for f in fournisseurs]
            return Response(data)
        
        serializer = FournisseurSerializer(fournisseurs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FournisseurSerializer(data=request.data)
        if serializer.is_valid():
            fournisseur = serializer.save()
            return Response({"message": "Fournisseur created", "id": fournisseur.id}, status=201)
        return Response(serializer.errors, status=400)

# Retrieve, Update and Delete == GET, PUT and DELETE
class FournisseurDetailView(APIView):
    def get_object(self, pk):
        try:
            return Fournisseur.objects.get(pk=pk)
        except Fournisseur.DoesNotExist:
            return None

    def get(self, pk):
        fournisseur = self.get_object(pk)
        if not fournisseur:
            return Response({"error": "Fournisseur not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = FournisseurSerializer(fournisseur)
        return Response(serializer.data)

    def put(self, request, pk):
        fournisseur = self.get_object(pk)
        if not fournisseur:
            return Response({"error": "Fournisseur not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = FournisseurSerializer(fournisseur, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Fournisseur updated"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        fournisseur = self.get_object(pk)
        if not fournisseur:
            return Response(
                {"error": "Fournisseur not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        fournisseur.delete()
        return Response(
            {"message": "Fournisseur deleted successfully"},
            status=status.HTTP_200_OK  # Or HTTP_204_NO_CONTENT if you prefer
        )


def liste_fournisseurs(request):
    fournisseurs = Fournisseur.objects.all()
    serializer = FournisseurSerializer(fournisseurs, many=True)
    return render(request, "gestiondata/listFour.html", {"fournisseurs": serializer.data})


def Fournisseurpage(request):
    return render(request, "gestiondata/fournisseur.html")



#-------------------------------Menu-------#--------------------------------------

def menu_page(request):
    return render(request, "gestiondata/menu.html")

# In views.py, add these classes near the Fournisseur views
class MenuListCreateView(APIView):
    def get(self, request):
        format = request.query_params.get('format', 'full')
        menus = Menu.objects.all()
        if format == 'minimal':
            data = [{'id': m.id, 'name': m.list_Menu} for m in menus]
            return Response(data)
        
        serializer = MenuSerializer(menus, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MenuSerializer(data=request.data)
        if serializer.is_valid():
            menu = serializer.save()
            return Response({"message": "Menu created", "id": menu.id}, status=201)
        return Response(serializer.errors, status=400)

class MenuDetailView(APIView):
    def get_object(self, pk):
        try:
            return Menu.objects.get(pk=pk)
        except Menu.DoesNotExist:
            return None

    def get(self, request, pk):
        menu = self.get_object(pk)
        if not menu:
            return Response({"error": "Menu not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = MenuSerializer(menu)
        return Response(serializer.data)

    def put(self, request, pk):
        menu = self.get_object(pk)
        if not menu:
            return Response({"error": "Menu not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = MenuSerializer(menu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Menu updated"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        menu = self.get_object(pk)
        if not menu:
            return Response(
                {"error": "Menu not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        menu.delete()
        return Response(
            {"message": "Menu deleted successfully"},
            status=status.HTTP_200_OK
        )




#-------------------------------Articles-------#--------------------------------------

@csrf_exempt
def create_article(request):
    if request.method == "POST":
        data = json.loads(request.body)
        article = Articles.objects.create(
            name=data["name"],
            price=data["price"],
            code_barre=data["code_barre"],
            Categorie_id=data["categorie"]
        )
        return JsonResponse({"message": "Article created", "id": article.id})
    return JsonResponse({"error": "Only POST allowed"}, status=405)

def articles_page(request):
    return render(request, "gestiondata/articles.html")

@csrf_exempt
def update_article(request, article_id):
    if request.method == "PUT":
        data = json.loads(request.body)
        try:
            article = Articles.objects.get(id=article_id)
            article.name = data["name"]
            article.price = data["price"]
            article.code_barre = data["code_barre"]
            article.Categorie_id = data["categorie"]
            article.save()
            return JsonResponse({"message": "Article mis à jour"})
        except Articles.DoesNotExist:
            return JsonResponse({"error": "Article introuvable"}, status=404)
    return JsonResponse({"error": "Méthode non autorisée"}, status=405)

@csrf_exempt
def delete_article(request, article_id):
    if request.method == "DELETE":
        try:
            article = Articles.objects.get(id=article_id)
            article.delete()
            return JsonResponse({"message": "Article supprimé"})
        except Articles.DoesNotExist:
            return JsonResponse({"error": "Article introuvable"}, status=404)
    return JsonResponse({"error": "Méthode non autorisée"}, status=405)


#-------------------------------url-------#--------------------------------------


@csrf_exempt
def create_url(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            fournisseur = Fournisseur.objects.get(id=data["four_url"])
            url = Url.objects.create(name_url=data["name_url"], four_url=fournisseur)
            return JsonResponse({"message": "URL créée", "id": url.id})
        except Fournisseur.DoesNotExist:
            return JsonResponse({"error": "Fournisseur introuvable"}, status=400)
    return JsonResponse({"error": "Méthode non autorisée"}, status=405)

def url_page(request):
    return render(request, "gestiondata/url.html")

#----------------------------------TypeMenu-------#--------------------------------------

@csrf_exempt
def create_typemenu(request):
    if request.method == "POST":
        data = json.loads(request.body)
        typemenu = TypeMenu.objects.create(name=data["name"])
        return JsonResponse({"message": "TypeMenu créé", "id": typemenu.id})
    return JsonResponse({"error": "Méthode non autorisée"}, status=405)



def typemenu_page(request):
    return render(request, "gestiondata/typemenu.html")



#----------------------------------Categorie-------#--------------------------------------
@csrf_exempt
def create_categorie(request):
    if request.method == "POST":
        data = json.loads(request.body)
        cat = Categorie.objects.create(name_cat=data["name_cat"])
        return JsonResponse({"message": "Catégorie créée", "id": cat.id})
    return JsonResponse({"error": "Méthode non autorisée"}, status=405)

def categorie_page(request):
    return render(request, "gestiondata/categorie.html")

#-----------------------------------selective ----------------------#--------------------
def get_categories(request):
    categories = Categorie.objects.all().values("id", "name_cat")
    return JsonResponse(list(categories), safe=False)


def get_fournisseurs(request):
    fournisseurs = Fournisseur.objects.all().values("id", "name")
    return JsonResponse(list(fournisseurs), safe=False)

def get_typemenus_and_urls(request):
    typemenus = list(TypeMenu.objects.all().values("id", "name"))
    urls = list(Url.objects.all().values("id", "name_url"))
    return JsonResponse({"typemenus": typemenus, "urls": urls})
