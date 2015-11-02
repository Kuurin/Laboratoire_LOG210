from django.contrib import admin

# Register your models here.
from .forms import *
from .models import *
from django.contrib.auth.models import User



class CooperativeAdmin(admin.ModelAdmin):
	list_display = ["nom", "adresse"]
	form = CooperativeForm
admin.site.register(Cooperative, CooperativeAdmin)

class LivreAdmin(admin.ModelAdmin):
	list_display = ["ISBN", "etat"]
	form = LivreForm
admin.site.register(Livre, LivreAdmin)
