from django import forms

from .models import *

	
class EtudiantForm(forms.ModelForm):
	class Meta: 
		model = Etudiant
		fields = ['email' , 'no_tel', 'password']
		
	def clean_no_tel(self):
		no_tel = self.cleaned_data.get('no_tel')
		c_no_tel = ''
		for char in no_tel:
			if char.isdigit():
				c_no_tel += str(char)
		if not len(c_no_tel)==10:
			raise forms.ValidationError("Veuillez entrer les 10 chiffres du numéro de téléphone")
		return c_no_tel
		
	
class GestionnaireForm(forms.ModelForm):
	class Meta: 
		model = Gestionnaire
		fields = ['email' , 'password']
	def clean_email(self):
		return self.cleaned_data.get('email')
	def clean_password(self):
		return self.cleaned_data.get('password')
		
		
class CooperativeForm(forms.ModelForm):
	class Meta: 
		model = Cooperative
		fields = ['nom' , 'adresse']
		
class LivreForm(forms.ModelForm):
	class Meta: 
		model = Livre
		fields = ['user', 'ISBN' , 'titre', 'auteur', 'nb_pages', 'prix_neuf', 'etat',]
	
	
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



			