from django.urls import path
from . import views

app_name = "gestiondata"

urlpatterns = [
    path("fournisseur", views.Fournisseurpage, name="fournisseur"),
    
    path('fournisseurs/', views.liste_fournisseurs, name='liste_fournisseurs'),

    path("create/", views.create_fournisseur),
    path ("update/<int:fournisseur_id>/",views.update_fournisseur),
    path("delete/<int:fournisseur_id>/", views.delete_fournisseur),
    



]




