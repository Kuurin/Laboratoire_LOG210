from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from .models import Gestionnaire

from .forms import EtudiantForm, GestionnaireForm, CooperativeForm, LivreForm, DescriptionLivreForm
# Create your views here.
def home(request):
	title = "Coopérative"
	context = {
		"title": title,
	}
	#add a form
	
	html = "home.html"
	
	return render(request, html, context)
	
def etudiant(request):
	title = "Étudiant"
	form = EtudiantForm(request.POST or None)
	#form = EtudiantForm(request.POST or None, initial={'email': title})
	context = {
		"title": title,
		"form": form
	}
	#add a form
	
	html = "etudiant.html"
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
	
	
	return render(request, html, context)
	
def gestionnaire(request):
	title = "Gestionnaire"
	form = GestionnaireForm(request.POST or None)
	html = "gestionnaire.html"
	
	#sign up
	if Gestionnaire.objects.count() is 0:
		message = "Veuillez créer un compte gestionnaire"
		if form.is_valid():
			title = "Gestionnaire login"
			instance = form.save()
			html = "gestionnairelogin.html"
	#signin
	else:
		form = GestionnaireForm(request.POST or None)
		html = "gestionnairelogin.html"
		message = "Veuillez vous connecter"
		g = Gestionnaire.objects.all()[0]
		#if g.email == form.cleaned_data.get("email") and g.password == form.cleaned_data.get("email"):
		#	title = "Création coopérative"
		#	message = "Vous êtes connecté. Créez maintenant une coopérative"
		#	form = CooperativeForm(None)
	
	context = {
		"title": title,
		"form": form,
		"message": message,
	}
	
	
	
	return render(request, html, context)
	
#def contact(request):
#	form = ContactForm(request.POST or None)
#	if form.is_valid():
#		#for key in form.cleaned_data:
#		#	print(form.cleaned_data.get(key))
#		form_email = form.cleaned_data.get("email")
#		form_message = form.cleaned_data.get("message")
#		form_full_name = form.cleaned_data.get("full_name")
#		
#		subject = "Site contact form"
#		from_email= settings.EMAIL_HOST_USER
#		to_email = [from_email, "doubleswordman@hotmail.com"]
#		contact_message = "%s: %s via %s"%(
#			form_full_name,
#			form_message, 
#			form_email)
#		
#		send_mail(subject, 
#			contact_message, 	
#			from_email, 
#			to_email, 
#			fail_silently=False)
#					
#		
#	context = {
#		"form":form,
#	}
#	return render(request, "forms.html", context)