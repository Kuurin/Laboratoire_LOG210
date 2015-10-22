from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
#un module de validation d'adresse courriel a été utilisé
#son utilisation a été expliquée à l'adresse suivante
#https://pypi.python.org/pypi/validate_email
#consultée le 16 octobre 2015
#L'information vient du Python Software Foundation [US]
from validate_email import validate_email
from EnvVirtuel.src.cooperative.models import Livre

class EtudiantRegistrationForm(UserCreationForm):
	
	class Meta:
		model = User
		fields = ('username', 'password1', 'password2')
	
	#validation phone number ou email	
	def clean_username(self):
		value = self.cleaned_data['username']
		#si c'est un email
		if '@' in value:
			#un module de validation d'adresse courriel a été utilisé
			#son utilisation a été expliquée à l'adresse suivante
			#https://pypi.python.org/pypi/validate_email
			#consultée le 16 octobre 2015
			#L'information vient du Python Software Foundation [US]
			if not validate_email(value):
				raise forms.ValidationError("Veuillez entrer une adresse courriel valide")
		#si c'est un numéro de téléphone	
		if '@' not in value:
			if len(value) is not 10 or not value.isnumeric():
					raise forms.ValidationError("Votre numéro doit être écrit avec 10 chiffres, sans aucun autre caractère.")
		return value
		
		
	
	def save(self,  commit=True):
		user = super(EtudiantRegistrationForm, self).save(commit=False)
		
		if commit:
			user.save()
			
		return user

class GestionnaireRegistrationForm(UserCreationForm):
	
	class Meta:
		model = User
		fields = ('username', 'password1', 'password2')
		
	#validation ou email	
	def clean_username(self):
		value = self.cleaned_data['username']
		#un module de validation d'adresse courriel a été utilisé
		#son utilisation a été expliquée à l'adresse suivante
		#https://pypi.python.org/pypi/validate_email
		#consultée le 16 octobre 2015
		#L'information vient du Python Software Foundation [US]
		if not validate_email(value):
			raise forms.ValidationError("Veuillez entrer une adresse courriel valide")
		return value
	
	
	def save(self,  commit=True):
		user = super(GestionnaireRegistrationForm, self).save(commit=False)
		
		if commit:
			user.save()
			
		return user
		
class AjoutLivreForm():
	
	class Meta:
		model = Livre
		fields = ('isbn', 'titre', 'auteur', 'prix')
		
	def clean_isbn(self):
		value = self.cleaned_data['isbn']
		if not 10 <= value.length <= 13 | value.isalnum():	
			raise forms.ValidationError("Veuillez entrer un ISBN/EAN/UPC valide")
		return value
	
	def clean_titre(self):
		value = self.cleaned_data['titre']
		return value
		
	def clean_auteur(self):
		value = self.cleaned_data['auteur']
		if not value.isalpha() & ' ' in value & "'" in value:
			raise forms.ValidationError("Veuillez entrer un nom valide")
		return value
		
		
		
		
		
		
		
		
		