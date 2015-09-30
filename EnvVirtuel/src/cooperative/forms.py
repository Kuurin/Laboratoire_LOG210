from django import forms

from .models import Etudiant, Gestionnaire, Cooperative, Livre, DescriptionLivre

	

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
		fields = ['ISBN' , 'etat', ]

class DescriptionLivreForm(forms.ModelForm):
	class Meta:
		model = DescriptionLivre
		fields = ['ISBN', 'titre', 'auteur', 'nb_pages', 'prix_neuf']
	def clean_nb_pages(self):
		c_nb_pages = float(self.cleaned_data.get('nb_pages'))
		if float(c_nb_pages)<1:
			raise forms.ValidationError("Veuillez entrer un nombre de pages valide")
		return c_nb_pages
	def clean_prix_neuf(self):
		c_prix_neuf = float(self.cleaned_data.get('prix_neuf'))
		if float(c_prix_neuf)<0.01:
			raise forms.ValidationError("Veuillez entrer un prix valide")
		return c_prix_neuf
			