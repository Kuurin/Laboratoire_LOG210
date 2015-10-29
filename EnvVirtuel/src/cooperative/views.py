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
			username=form.cleaned_data['username']
			Argent.creer_bourse(username,"1000")
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
	if request.user.is_authenticated and not request.user.is_staff:
		argent = Argent.objects.get(username=request.user.username)
	else:
		argent = ""
	message = "Ici vont se trouver les options pour les étudiants"
	
	context = {
		"title": title,
		"message":message,
		"argent":argent,
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
	if request.user.is_authenticated and not request.user.is_staff:
		argent = Argent.objects.get(username=request.user.username)
	else:
		argent = ""
	form = LivreForm(request.POST or None)
	html = "ajouterlivre.html"
	
	form.cacher_desc()
	
	context = {
		"title": title,
		"form": form,
		"argent":argent,
	}
	context.update(csrf(request))
	
	return  render(request, html, context)
	

def ajouterlivredescription(request):
	title = "Ajouter la description du livre"
	if request.user.is_authenticated and not request.user.is_staff:
		argent = Argent.objects.get(username=request.user.username)
	else:
		argent = ""
	form = LivreForm(request.POST or None)
	
	
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		context = {
			"title": title,
			"message": 'Vous avez ajouté un livre avec succès',
			"argent":argent,
		}
		context.update(csrf(request))
		html = 'register_success.html'
		return  render(request, html, context)

	isbn = form.cleaned_data['ISBN']
	form = LivreForm(None, initial={'user':request.user.username, 'ISBN':isbn,"titre": isbnlib.get_titre(isbn),"auteur": isbnlib.get_auteur(isbn),"nb_pages": isbnlib.get_pages(isbn),"prix_neuf": isbnlib.get_prix(isbn),})
	
	form.block_isbn()
	
	html = "ajouterlivre.html"
	context = {
		"title": title,
		"form": form,
		"argent":argent,
	}
	context.update(csrf(request))
	
	return  render(request, html, context)
	
def etudiantvoirlivres(request):
	user_id = request.user.id
	if request.user.is_authenticated and not request.user.is_staff:
		argent = Argent.objects.get(username=request.user.username)
	else:
		argent = ""
	title = "Livres non-éditables :"
	livres = Livre.objects.filter(user=request.user.username)
	livres = livres.exclude(recu="0")
	
	message=""
	for l in livres:
		message = message + str(l) + "\n"
	
	livres = Livre.objects.filter(user=request.user.username)
	if len(livres.filter(recu="0"))>0:
		title =""
		g_form = GestionLivreForm(livres.filter(recu="0"))
		g_form.fields['livres'].label = "Livre(s) éditable(s):"
	else :
		g_form = "aucun"
	
	html = "etudiantvoirlivres.html"
	context = {
		"title": title,
		"form": g_form,
		"message": message,
		"argent":argent,
	}
	context.update(csrf(request))
	
	return  render(request, html, context)	
	
def etudiantvoirreserves(request):
	title = "Livre(s) réservé(s) :"
	if request.user.is_authenticated and not request.user.is_staff:
		argent = Argent.objects.get(username=request.user.username)
	else:
		argent = ""
	livres = Livre.objects.filter(acheteur=request.user.username).filter(recu="0.50")
	
	message=""
	
	if len(livres)>0:
		title =""
		g_form = GestionLivreForm(livres)
		g_form.fields['livres'].label = "Livre(s) réservé(s):"
	else :
		g_form = "aucun"
	
	html = "etudiantvoirreserves.html"
	context = {
		"title": title,
		"form": g_form,
		"message": message,
		"argent":argent,
	}
	context.update(csrf(request))
	
	return  render(request, html, context)	
	
def etudiantvoirachetes(request):
	title = "Livre(s) acheté(s) :"
	if request.user.is_authenticated and not request.user.is_staff:
		argent = Argent.objects.get(username=request.user.username)
	else:
		argent = ""
	livres = Livre.objects.filter(acheteur=request.user.username).filter(recu="0.75")
	
	message=""
	
	if len(livres)>0:
		title =""
		g_form = GestionLivreForm(livres)
		g_form.fields['livres'].label = "Livre(s) acheté(s) à récupérer:"
	else :
		g_form = "aucun"
	
	html = "etudiantvoirachetes.html"
	context = {
		"title": title,
		"form": g_form,
		"message": message,
		"argent":argent,
	}
	context.update(csrf(request))
	
	return  render(request, html, context)
	
def etudiantvoirofferts(request):
	title = 'Gestion des livres à la coopérative'
	if request.user.is_authenticated and not request.user.is_staff:
		argent = Argent.objects.get(username=request.user.username)
	else:
		argent = ""
	message = ''
	
	r_form = RechercheForm(request.POST or None)
	LIVRES_TROUVES = r_form.chercher()
	r_form.cacher()

	livres_dispo = LIVRES_TROUVES.exclude(recu="1").exclude(recu="0.75").exclude(recu="0.50").exclude(recu="0").exclude(user=request.user)
	if len(livres_dispo)>0:
		g_form = GestionLivreForm(livres_dispo)
		g_form.fields['livres'].label = "Livres à éditer:"
	else :
		g_form = "aucun"
		message = "Rien n'a été trouvé "
		
	html = "etudiantvoirofferts.html"
	context = {
		"title": title,
		"message": message, 
		"form" : g_form,
		"r_form":r_form,
		"argent":argent,
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
	if request.POST.get("name") == "Réserver le livre":
		return reserverlivre(request)
	if request.POST.get("name") == "Acheter le livre" or request.POST.get("name") == "Confirmer l'achat":
		return acheterlivre(request)
	if request.POST.get("name") == "Annuler la réservation":
		return dereserverlivre(request)
	if request.POST.get("name") == "Livrer le livre":
		return livrerlivre(request)
	if request.POST.get("name") == "Annuler transaction":
		return annulertransaction(request)	
	return home(request)
def reserverlivre(request):
	title = "Réservation d'un livre"
	if request.user.is_authenticated and not request.user.is_staff:
		argent = Argent.objects.get(username=request.user.username)
	else:
		argent = ""
	livre = Livre.objects.get(id=request.POST.get('livres'))
	message = "Le livre a été réservé : " + str(livre)
	form = LivreForm(None, initial={'iden':livre.id})
	form.cacher()
	livre.reserver(request.user)
	html = "etudiantreserverlivre.html"
	context = {
		"title": title,
		"message": message, 
		"form" : form,
		"argent":argent,
	}
	context.update(csrf(request))
	return  render(request, html, context)

def livrerlivre(request):
	livre = Livre.objects.get(id=request.POST.get('livres'))
	livre.livrer()
	if not request.user.is_staff:
		return etudiantvoirlivres(request)
	if request.user.is_staff:
		return gestionnairevoirlivres(request)	
	
def annulertransaction(request):
	livre = Livre.objects.get(id=request.POST.get('livres'))
	livre.annulertransaction()
	if not request.user.is_staff:
		return etudiantvoirlivres(request)
	if request.user.is_staff:
		return gestionnairevoirlivres(request)	
	
def dereserverlivre(request):
	title = "Achat d'un livre"
	if request.user.is_authenticated and not request.user.is_staff:
		argent = Argent.objects.get(username=request.user.username)
	else:
		argent = ""
	livre = Livre.objects.get(id=request.POST.get('iden') or request.POST.get('livres'))
	livre.dereserver(request.user)
	return etudiantvoirreserves(request)
	
def acheterlivre(request):
	title = "Achat d'un livre"
	if request.user.is_authenticated and not request.user.is_staff:
		argent = Argent.objects.get(username=request.user.username)
	else:
		argent = ""
	livre = Livre.objects.get(id=request.POST.get('iden') or request.POST.get('livres'))
	
	livre.acheter(request.user)
	message = "Le livre a été acheté. Il est prêt à être récupéré. : " + str(livre)
	form = LivreForm(None, initial={'iden':livre.id})
	form.cacher()
	html = "etudiantacheterlivre.html"
	context = {
		"title": title,
		"message": message, 
		"form" : form,
		"argent":argent,
	}
	context.update(csrf(request))
	return  render(request, html, context)
	
def dupliquerlivre(request):
	livre = Livre.objects.get(id=request.POST.get('livres'))
	livre.dupliquer()
	if not request.user.is_staff:
		return etudiantvoirlivres(request)
	if request.user.is_staff:
		return gestionnairevoirlivres(request)
	
def modifierlivre(request):
	title = 'Livre à modifier'
	if request.user.is_authenticated and not request.user.is_staff:
		argent = Argent.objects.get(username=request.user.username)
	else:
		argent = ""
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
	form.block_isbn()
	html = "modifierlivre.html"
	
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		message = 'Le livre a été modifié'
		form = "aucun"
		title = "Livre modifié"
		message = "Le livre a été modifié"
		if not request.user.is_staff:
			return etudiantvoirlivres(request)
		if request.user.is_staff:
			return gestionnairevoirlivres(request)
		
	context = {
		"title":title,
		"message":message,
		"form":form,
		"r_form":r_form,
		"argent":argent,
		}
	context.update(csrf(request))
	return  render(request, html, context)
	
def supprimerlivre(request):
	livre = Livre.objects.get(id=request.POST.get('livres'))
	livre.supprimer()
	if not request.user.is_staff:
		return etudiantvoirlivres(request)
	if request.user.is_staff:
		return gestionnairevoirlivres(request)

def recherche(request):
	title = 'Recherche de livres à la coopérative'
	if request.user.is_authenticated and not request.user.is_staff:
		argent = Argent.objects.get(username=request.user.username)
	else:
		argent = ""
	message = 'Veuillez entrer vos critères de recherche ou rien pour accéder à tout'

	form = RechercheForm(None)
	if not request.user.is_staff:
		form.fields['r_recu'].widget = form.fields['r_auteur'].hidden_widget()
	html = "recherche.html"
	context = {
		"title": title,
		"message": message, 
		"form" : form,
		"argent":argent,
	}
	context.update(csrf(request))
	return  render(request, html, context)
	
def gestionnairevoirlivres(request):
	title = 'Gestion des livres à la coopérative'
	message = ''
	
	r_form = RechercheForm(request.POST or None)
	LIVRES_TROUVES = r_form.chercher()
	r_form.cacher()
	
	if len(LIVRES_TROUVES)>0:
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