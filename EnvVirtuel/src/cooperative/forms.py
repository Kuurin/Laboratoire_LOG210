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
	
	def clean_ISBN(self):
		isbn = self.cleaned_data.get('ISBN')
		c_isbn = ""
		for c in isbn:
			if c.isdigit():
				c_isbn=c_isbn+c
		return c_isbn
		
	def clean_nb_pages(self):
		nb_pages = self.cleaned_data.get('nb_pages')
		if nb_pages<1:
			raise forms.ValidationError("Le nombre de pages doit être supérieur à 0")
		return nb_pages
		
	
	def clean_prix_neuf(self):
		try:
			c_prix_neuf = float(self.cleaned_data.get('prix_neuf'))
			if c_prix_neuf<0.01:
				raise forms.ValidationError("Le prix doit être supérieur à 0$")
			return c_prix_neuf
		except:
			raise forms.ValidationError("Le prix doit être un réel")
	
		
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
			livres = self.filtrer(livres,"ISBN",c_code)
		if len(c_titre) is not 0:
			livres = self.filtrer(livres,"titre",c_titre)
		if len(c_user) is not 0:
			livres = self.filtrer(livres,"user",c_user)
		return livres
	def contains(self,exp, str):
		exp = exp.lower()
		str = str.lower()
		if exp in str:
			return True
		else:
			return False
	def filtrer(self,livres,critere,exp):
		if critere == "ISBN":
			for l in livres:
				if not self.contains(exp, l.ISBN):
					livres = livres.exclude(id=l.id)
		if critere == "titre":
			for l in livres:
				if not self.contains(exp, l.titre):
					livres = livres.exclude(id=l.id)
		if critere == "user":
			for l in livres:
				if not self.contains(exp, l.user):
					livres = livres.exclude(id=l.id)
		return livres


class GestionLivreForm(forms.Form):
	def __init__(self, livres, *args, **kwargs):
		super(GestionLivreForm, self).__init__(*args, **kwargs)
		if len(livres)>=1:
			livres = livres.order_by('user')
			self.fields['livres'] = forms.ModelChoiceField(queryset=livres, initial=livres[0], widget=forms.RadioSelect())
	
