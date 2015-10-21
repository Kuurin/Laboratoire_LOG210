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

from .forms import EtudiantForm,GestionnaireForm, CooperativeForm, LivreForm, DescriptionLivreForm
# Create your views here.


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


#ame
def remise(request):
	
	
	return render(request,"remise.html",{})
	
	
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