import json
from django.http import JsonResponse
from django.shortcuts import render
from gestiondata.models import Fournisseur
from django.views.decorators.csrf import csrf_exempt
# Create your views here.




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