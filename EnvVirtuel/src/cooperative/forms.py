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
		fields = ['user', 'ISBN' , 'titre', 'auteur', 'nb_pages', 'prix_neuf', 'etat']

class RechercheForm(forms.Form):
	code = forms.CharField(label='Code', max_length=20)
	titre = forms.CharField(label='Titre', max_length=200)
	user_id = forms.CharField(label="Identifiant d'utilisateur", max_length=100)
	
	def chercher(self):
		livres = Livre.objects.all()
		c_code = self.data.get('code')
		c_titre = self.data.get('titre')
		c_user = self.data.get('user_id')
		if len(c_code) is not 0:
			livres = livres.filter(ISBN=c_code)
		if len(c_titre) is not 0:
			livres = livres.filter(titre=c_titre)
		if len(c_user) is not 0:
			livres = livres.filter(user=c_user)
		return livres


class GestionLivreForm(forms.Form):
	def __init__(self, livres, *args, **kwargs):
		super(GestionLivreForm, self).__init__(*args, **kwargs)
		if len(livres)>=1:
			self.fields['livres'] = forms.ModelChoiceField(queryset=livres, initial=livres[0], widget=forms.RadioSelect())
	
			
	#def __init__(self, livres, *args, **kwargs):
	#	super(GestionLivreForm, self).__init__(*args, **kwargs)
	#	self.fields['livres'] =  forms.ModelMultipleChoiceField(queryset=livres,widget=forms.CheckboxSelectMultiple())