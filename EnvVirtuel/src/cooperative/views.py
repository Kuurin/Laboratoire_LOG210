from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from .models import Gestionnaire

#pour login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

#pour register
#from django.contrib.auth.forms import UserCreationForm
from projet_log210.forms import EtudiantRegistrationForm, GestionnaireRegistrationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib import auth
from django.core.context_processors import csrf

from .forms import *
# Create your views here.

import isbnlib

def home(request):
	title = "Coopérative"
	context = {
		"title": title,
		'user':request.user,
	}
	#add a form
	
	html = "home.html"
	
	return render(request, html, context) 
	
#register

def register_user_etudiant(request):
	form = EtudiantRegistrationForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/register_success/')
		else: 
			args = {}
			args.update(csrf(request))
			args ['form'] = form
			return render(request, 'registeretudiant.html' , args)
	else:
		args = {}
		args.update(csrf(request))
		args ['form'] = EtudiantRegistrationForm()
		return render_to_response ('registeretudiant.html', args)
	
def register_user_gestionnaire(request):
	if not len(User.objects.filter(is_staff=True)) == 1:
		args = {"title": 'Coopérative',
		'user':request.user,"message":"Il ne peut y avoir qu'un seul gestionnaire."}
		args.update(csrf(request))
		return render(request, 'home.html' , args)
	form = GestionnaireRegistrationForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			u=User.objects.get(username=form.cleaned_data['username'])
			u.is_staff=True;
			u.save()
			return HttpResponseRedirect('/registercoop/')
		else: 
			args = {}
			args.update(csrf(request))
			args ['form'] = form
			return render(request, 'registergestionnaire.html' , args)
	else:
		args = {}
		args.update(csrf(request))
		args ['form'] = form
		return render_to_response ('registergestionnaire.html', args)

def register_success(request):
	return render_to_response('register_success.html')
	

def registercoop(request):
	title = "Enregistrer la coopérative"
	form = CooperativeForm(request.POST or None)
	context = {
		"title": title,
		"form": form
	}
	context.update(csrf(request))
	
	html = "registergen.html"
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		return HttpResponseRedirect('/register_success/')
	
	
	return render(request, html, context)
	
def optionsetudiant(request):
	title = "Étudiant"
	html = "optionsetudiant.html"
	message = "Ici vont se trouver les options pour les étudiants"
	
	context = {
		"title": title,
		"message":message,
	}
	return render(request, html, context)
	
def optionsgestionnaire(request):
	title = "Gestionnaire"
	html = "optionsgestionnaire.html"
	message = "Ici vont se trouver les options pour le gestionnaire"
	
	context = {
		"title": title,
		"message": message,
	}
	return render(request, html, context)
	

def ajouterlivre(request):
	title = "Ajouter le livre"
	form = LivreForm(request.POST or None)
	html = "ajouterlivre.html"
	
	#Morceau de code emprunté à l'adresse 
	#http://stackoverflow.com/questions/1255976/how-do-you-dynamically-hide-form-fields-in-django
	#consulté le 24-10-2015, réponse de Jason Christa en 2012
	form.fields['user'].widget = form.fields['user'].hidden_widget()
	form.fields['titre'].widget = form.fields['titre'].hidden_widget()
	form.fields['auteur'].widget = form.fields['auteur'].hidden_widget()
	form.fields['nb_pages'].widget = form.fields['nb_pages'].hidden_widget()
	form.fields['prix_neuf'].widget = form.fields['prix_neuf'].hidden_widget()
	form.fields['etat'].widget = form.fields['etat'].hidden_widget()
	
	context = {
		"title": title,
		"form": form
	}
	context.update(csrf(request))
	
	return  render(request, html, context)
	

def ajouterlivredescription(request):
	title = "Ajouter la description du livre"
	form = LivreForm(request.POST or None)
	
	
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		context = {
			"title": title,
			"message": 'Vous avez ajouté un livre avec succès',
		}
		context.update(csrf(request))
		html = 'register_success.html'
		return  render(request, html, context)

	isbn = form.cleaned_data['ISBN']
	form = LivreForm(None, initial={'user':request.user.username, 'ISBN':isbn,"titre": isbnlib.get_titre(isbn),"auteur": isbnlib.get_auteur(isbn),"nb_pages": isbnlib.get_pages(isbn),"prix_neuf": isbnlib.get_prix(isbn),})
	form.fields['user'].widget = form.fields['user'].hidden_widget()
	
	#Morceau de code emprunté à l'adresse 
	#http://stackoverflow.com/questions/4945802/how-can-i-disable-a-model-field-in-a-django-form
	#consulté le 24-10-2015, réponse de Yuji 'Tomita' Tomita en 2011
	form.fields['ISBN'].widget.attrs['readonly'] = True # text input
	
	html = "ajouterlivre.html"
	context = {
		"title": title,
		"form": form,
	}
	context.update(csrf(request))
	
	return  render(request, html, context)
	
def voirlivresetudiant(request):
	user_id = request.user.id
	title = "Livres non-éditables :"
	livres = Livre.objects.filter(user=request.user.username)
	livres = livres.exclude(recu="0")
	
	message=""
	for l in livres:
		message = message + str(l) + "\n"
	
	livres = Livre.objects.filter(user=request.user.username)
	if len(livres.filter(recu="0"))>0:
		g_form = GestionLivreForm(livres.filter(recu="0"))
		g_form.fields['livres'].label = "Livre(s) éditable(s):"
	else :
		g_form = "aucun"
	
	html = "voirlivresetudiant.html"
	context = {
		"title": title,
		"form": g_form,
		"message": message,
	}
	context.update(csrf(request))
	
	return  render(request, html, context)
def actionlivre(request):
	if request.POST.get("name") == "Supprimer le livre":
		return supprimerlivre(request)
	if request.POST.get("name") == "Dupliquer le livre":
		return dupliquerlivre(request)
	if request.POST.get("name") == "Modifier le livre":
		return modifierlivre(request)
	if request.POST.get("name") == "Confirmer l'état puis recevoir":
		return gestionnairerecus(request)	
	return home(request)

def dupliquerlivre(request):
	livre = Livre.objects.get(id=request.POST.get('livres'))
	livre.dupliquer()
	if not request.user.is_staff:
		return voirlivresetudiant(request)
	if request.user.is_staff:
		return gestionnairevoirlivres(request)
	
def modifierlivre(request):
	title = 'Livre à modifier'
	message = 'Veuillez modifier les champs voulus'
	
	r_form = RechercheForm(request.POST or None)
	LIVRES_TROUVES = r_form.chercher()
	r_form.cacher()
	
	try:
		livre = Livre.objects.get(id=request.POST.get('livres'))
		form = LivreForm(None ,initial={'user':livre.user, 'ISBN':livre.ISBN, 'titre':livre.titre, 'auteur':livre.auteur, 'nb_pages':livre.nb_pages,'prix_neuf':livre.prix_neuf,'etat':livre.etat,})
		livre.supprimer()
	except:
		form = LivreForm(request.POST or None)
	form.fields['user'].widget = form.fields['user'].hidden_widget()
	form.fields['ISBN'].widget.attrs['readonly'] = True # text input
	html = "modifierlivre.html"
	
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		message = 'Le livre a été modifié'
		form = "aucun"
		title = "Livre modifié"
		message = "Le livre a été modifié"
		if not request.user.is_staff:
			return voirlivresetudiant(request)
		if request.user.is_staff:
			return gestionnairevoirlivres(request)
		
	context = {
		"title":title,
		"message":message,
		"form":form,
		"r_form":r_form,
		}
	context.update(csrf(request))
	return  render(request, html, context)
	
def supprimerlivre(request):
	livre = Livre.objects.get(id=request.POST.get('livres'))
	livre.supprimer()
	if not request.user.is_staff:
		return voirlivresetudiant(request)
	if request.user.is_staff:
		return gestionnairevoirlivres(request)


def gestionnairerecherche(request):
	title = 'Recherche des livres à la coopérative'
	message = 'Veuillez entrer vos critères de recherche ou rien pour accéder à tout'

	form = RechercheForm(None)
	html = "gestionnairerecherche.html"
	context = {
		"title": title,
		"message": message, 
		"form" : form
	}
	context.update(csrf(request))
	return  render(request, html, context)
	
def gestionnairevoirlivres(request):
	title = 'Gestion des livres à la coopérative'
	message = ''
	
	r_form = RechercheForm(request.POST or None)
	LIVRES_TROUVES = r_form.chercher()
	r_form.cacher()
	
	if len(LIVRES_TROUVES.filter(recu="0"))>0:
		g_form = GestionLivreForm(LIVRES_TROUVES)
		g_form.fields['livres'].label = "Livres à éditer:"
	else :
		g_form = "aucun"
		message = "Rien n'a été trouvé "
		
	html = "gestionnairevoirlivres.html"
	context = {
		"title": title,
		"message": message, 
		"form" : g_form,
		"r_form":r_form,
	}
	context.update(csrf(request))
	return  render(request, html, context)
	
def gestionnairerecus(request):
	title = 'Livre reçu'
	message = 'Voici le livre dont le statut a été changé: \n'
	

	livre = Livre.objects.get(id=request.POST.get('livres'))
	
	livre.remettre()
	message = message + str(livre) + "\n"
	
	html = "optionsgestionnaire.html"
	context = {
		"title": title,
		"message": message, 
	}
	context.update(csrf(request))
	return  gestionnairevoirlivres(request)
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