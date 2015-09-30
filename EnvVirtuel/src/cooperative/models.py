from django.db import models
import decimal

# Create your models here.
class Etudiant(models.Model):
	email = models.EmailField(blank=True, null=True)
	besoinTel = not email.clean
	no_tel = models.CharField(max_length=20, blank=True, null=True)
	password = models.CharField(max_length=120, blank=False, null=True)
	
	def __str__(self): 
		return self.email
		
class Gestionnaire(models.Model):
	email = models.EmailField()
	password = models.CharField(max_length=120, blank=False, null=True)
	def __str__(self):
		return self.email

class Cooperative(models.Model):
	nom = models.CharField(max_length=120, blank=False, null=True)
	adresse = models.CharField(max_length=1000, blank=False, null=True)
	
	def __str__(self):
		return self.nom
		
		
class DescriptionLivre(models.Model):
	ISBN = models.CharField(max_length=16, blank=False, null=True)
	titre = models.CharField(max_length=120, blank=False, null=True)
	auteur = models.CharField(max_length=120, blank=False, null=True)
	nb_pages = models.IntegerField()
	prix_neuf = models.CharField(max_length=14, blank=False, null=True)
	
	def __str__(self):
		return self.ISBN
		
		
class Livre(models.Model):
	ISBN = models.CharField(max_length=16, blank=False, null=True)
	etat_choix = (('0.75' , 'Comme neuf'), ('0.50' , 'Peu usé'), ('0.25', 'Très usé'), )
	#prix 
	etat = models.CharField(max_length=4,choices=etat_choix, default = '0.75')
	
	def __str__(self):
		return self.ISBN
		
