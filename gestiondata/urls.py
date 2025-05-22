from django.urls import path
from . import views

app_name = "gestiondata"

urlpatterns = [
#----------------------------------Pages----#--------------------------------------
    path("fournisseur", views.Fournisseurpage, name="fournisseur"),
    path("menu", views.menu_page, name="menu_page"),
    path("articles", views.articles_page, name="articles_page"), 
    path("url", views.url_page, name="url_page"),
    path("typemenu", views.typemenu_page, name="typemenu_page"),  
    path("categorie/", views.categorie_page, name="categorie_page"),

#----------------------------------Affichage-------#--------------------------------------
    path('fournisseurs/', views.liste_fournisseurs, name='liste_fournisseurs'),
#----------------------------------CRUD ENDPOINTS-------#--------------------------------------
    path("create/", views.create_fournisseur),
    path ("update/<int:fournisseur_id>/",views.update_fournisseur),
    path("delete/<int:fournisseur_id>/", views.delete_fournisseur),
    path("create_menu/", views.create_menu),
    path("create_article/", views.create_article),
    path("create_url/", views.create_url),
    path("create_typemenu/", views.create_typemenu),
    path("create_categorie/", views.create_categorie),
#----------------------------------Selective button----#--------------------------------------
    path("api/fournisseurs/", views.get_fournisseurs),
    path("api/typemenus_urls/", views.get_typemenus_and_urls),
    path("api/categories/", views.get_categories),


]




