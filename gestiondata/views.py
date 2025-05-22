import json
from django.http import JsonResponse
from django.shortcuts import render
from gestiondata.models import Fournisseur,Menu,Articles,TypeMenu,Url,Categorie
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


#----------------------------------Fournisseur----#--------------------------------------

def liste_fournisseurs(request):
    fournisseurs= Fournisseur.objects.all()
    return render(request, "gestiondata/listFour.html", {"fournisseurs": fournisseurs})


def Fournisseurpage(request):
    return render(request, "gestiondata/fournisseur.html")


def create_fournisseur(request):
    if request.method == "POST":
        data = json.loads(request.body)
        fournisseur = Fournisseur.objects.create(
            name=data["name"],
            localisation = data["localisation"],
            address = data["address"],
            type = data["type"],
            domaine = data["domaine"],
            phone = data["phone"],
            email = data["email"],
            art = data["art"],
            nis = data["nis"],
            nif = data["nif"]
        )
        return JsonResponse({"message": "fournisseur created", "id": fournisseur.id})
    return JsonResponse({"error": "Only POST allowed"}, status=405)


@csrf_exempt
def update_fournisseur(request, fournisseur_id):
    if request.method == "PUT":
        data = json.loads(request.body)
        try:
            fournisseur = Fournisseur.objects.get(pk=fournisseur_id)
            fournisseur.name = data["name"]
            fournisseur.localisation = data["localisation"]
            fournisseur.address = data["address"]
            fournisseur.type = data["type"]
            fournisseur.domaine = data["domaine"]
            fournisseur.phone = data["phone"]
            fournisseur.email = data["email"]
            fournisseur.art = data["art"]
            fournisseur.nis = data["nis"] 
            fournisseur.nif = data["nif"]
            fournisseur.save()
            return JsonResponse({"message": "Fournisseur updated"})
        except Fournisseur.DoesNotExist:
            return JsonResponse({"error": "Fournisseur not found"}, status=404)
    return JsonResponse({"error": "Only PUT allowed"}, status=405)

@csrf_exempt
def delete_fournisseur(request, fournisseur_id):
    if request.method == "DELETE":
        try:
            fournisseur = Fournisseur.objects.get(pk=fournisseur_id)
            fournisseur.delete()
            return JsonResponse({"message": "Fournisseur deleted"})
        except Fournisseur.DoesNotExist:
            return JsonResponse({"error": "Fournisseur not found"}, status=404)
    return JsonResponse({"error": "Only DELETE allowed"}, status=405)



#-------------------------------Menu-------#--------------------------------------


@csrf_exempt
def create_menu(request):
    if request.method == "POST":
        data = json.loads(request.body)
        menu = Menu.objects.create(
            list_Menu=data["list_Menu"],
           # list_Price=data["list_Price"],
            extension=data.get("extension"),
            type_menu_id=data["type_menu"],
            Url_id=data["url"]
        )
        return JsonResponse({"message": "Menu created", "id": menu.id})
    return JsonResponse({"error": "Only POST allowed"}, status=405)


def menu_page(request):
    return render(request, "gestiondata/menu.html")


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
