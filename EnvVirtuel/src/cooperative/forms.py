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
	iden = forms.CharField(label='Code', max_length=20,required=False)
	class Meta: 
		model = Livre
		fields = ['user', 'ISBN' , 'titre', 'auteur', 'nb_pages', 'prix_neuf', 'etat']
	
	def __init__(self, *args, **kwargs):
		super(LivreForm, self).__init__(*args, **kwargs)
		self.fields['user'].widget = self.fields['user'].hidden_widget()
		self.fields['iden'].widget = self.fields['iden'].hidden_widget()
	def cacher(self):
		self.fields['ISBN'].widget = self.fields['ISBN'].hidden_widget()
		self.fields['user'].widget = self.fields['user'].hidden_widget()
		self.fields['titre'].widget = self.fields['titre'].hidden_widget()
		self.fields['auteur'].widget = self.fields['auteur'].hidden_widget()
		self.fields['nb_pages'].widget = self.fields['nb_pages'].hidden_widget()
		self.fields['prix_neuf'].widget = self.fields['prix_neuf'].hidden_widget()
		self.fields['etat'].widget = self.fields['etat'].hidden_widget()
		self.fields['ISBN'].required = False
		self.fields['user'].required = False
		self.fields['titre'].required = False
		self.fields['auteur'].required = False
		self.fields['nb_pages'].required = False
		self.fields['prix_neuf'].required = False
		self.fields['etat'].required = False
		
	def cacher_desc(self):
		#Morceau de code emprunté à l'adresse 
		#http://stackoverflow.com/questions/1255976/how-do-you-dynamically-hide-form-fields-in-django
		#consulté le 24-10-2015, réponse de Jason Christa en 2012
		self.fields['user'].widget = self.fields['user'].hidden_widget()
		self.fields['titre'].widget = self.fields['titre'].hidden_widget()
		self.fields['auteur'].widget = self.fields['auteur'].hidden_widget()
		self.fields['nb_pages'].widget = self.fields['nb_pages'].hidden_widget()
		self.fields['prix_neuf'].widget = self.fields['prix_neuf'].hidden_widget()
		self.fields['etat'].widget = self.fields['etat'].hidden_widget()
	def block_isbn(self):
		#Morceau de code emprunté à l'adresse 
		#http://stackoverflow.com/questions/4945802/how-can-i-disable-a-model-field-in-a-django-form
		#consulté le 24-10-2015, réponse de Yuji 'Tomita' Tomita en 2011
		self.fields['ISBN'].widget.attrs['readonly'] = True # text input
	
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
	code = forms.CharField(label='Code', max_length=20,required=False)
	r_titre = forms.CharField(label='Titre', max_length=200,required=False)
	user_id = forms.CharField(label="Identifiant d'utilisateur", max_length=100,required=False)
	r_auteur = forms.CharField(label='Auteur', max_length=200,required=False)
	#s'il est reçu 
	recu_choix = (('', 'Non spécifié'), ('0' , 'Avec le vendeur'), ('0.25' , 'A la cooperative'), ('0.50' , 'Reserve'), ('0.75' , 'Achete'), ('1' , "Delivre à l'acheteur"),)
	r_recu = forms.ChoiceField(choices=recu_choix, label="Étape", required=False)
	
	
	def cacher(self):
		self.fields['code'].widget = self.fields['code'].hidden_widget()
		self.fields['r_titre'].widget = self.fields['r_titre'].hidden_widget()
		self.fields['user_id'].widget = self.fields['user_id'].hidden_widget()
		self.fields['r_auteur'].widget = self.fields['r_auteur'].hidden_widget()
		self.fields['r_recu'].widget = self.fields['r_auteur'].hidden_widget()
	def chercher(self):
		livres = Livre.objects.all()
		c_code = self.data.get('code')
		c_titre = self.data.get('r_titre')
		c_user = self.data.get('user_id')
		c_r_auteur = self.data.get('r_auteur')
		c_r_recu = self.data['r_recu']
		print(c_r_recu)
		if c_code is not None:
			livres = self.filtrer(livres,"ISBN",c_code)
		if c_titre is not None:
			livres = self.filtrer(livres,"r_titre",c_titre)
		if c_user is not None:
			livres = self.filtrer(livres,"user",c_user)
		if c_r_auteur is not None:
			livres = self.filtrer(livres,"r_auteur",c_r_auteur)
		if not c_r_recu == '':
			livres = self.filtrer(livres,"r_recu",c_r_recu)
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
		if critere == "r_titre":
			for l in livres:
				if not self.contains(exp, l.titre):
					livres = livres.exclude(id=l.id)
		if critere == "user":
			for l in livres:
				if not self.contains(exp, l.user):
					livres = livres.exclude(id=l.id)
		if critere == "r_auteur":
			for l in livres:
				if not self.contains(exp, l.auteur):
					livres = livres.exclude(id=l.id)
		if critere == "r_recu":
			livres = livres.filter(recu=exp)
		return livres


class GestionLivreForm(forms.Form):
	def __init__(self, livres, *args, **kwargs):
		super(GestionLivreForm, self).__init__(*args, **kwargs)
		if len(livres)>=1:
			livres = livres.order_by('user')
			self.fields['livres'] = forms.ModelChoiceField(queryset=livres, initial=livres[len(livres)-1], widget=forms.RadioSelect())
	
