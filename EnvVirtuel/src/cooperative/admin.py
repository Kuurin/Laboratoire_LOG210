from django.contrib import admin

# Register your models here.
from .forms import *
from .models import *


class EtudiantAdmin(admin.ModelAdmin):
	list_display = ["email", "no_tel"]
	form = EtudiantForm
	
admin.site.register(Etudiant, EtudiantAdmin)

class GestionnaireAdmin(admin.ModelAdmin):
	list_display = ["email"]
	form = GestionnaireForm
admin.site.register(Gestionnaire, GestionnaireAdmin)

class CooperativeAdmin(admin.ModelAdmin):
	list_display = ["nom", "adresse"]
	form = CooperativeForm
admin.site.register(Cooperative, CooperativeAdmin)

class LivreAdmin(admin.ModelAdmin):
	list_display = ["ISBN", "etat"]
	form = LivreForm
admin.site.register(Livre, LivreAdmin)
