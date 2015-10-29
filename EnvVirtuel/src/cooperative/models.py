from django.db import models
import decimal

from django.contrib.auth.models import User

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
		
		
		
class Livre(models.Model):
	user = models.CharField(max_length=120, blank=True, null=True)
	acheteur = models.CharField(max_length=120, blank=True, null=True, default="")

	ISBN = models.CharField(max_length=16, blank=False, null=True)
	titre = models.CharField(max_length=120, blank=False, null=True)
	auteur = models.CharField(max_length=120, blank=False, null=True)
	nb_pages = models.IntegerField(default=1)
	prix_neuf = models.CharField(max_length=14, blank=False, null=True)
	#prix 
	etat_choix = (('0.75' , 'Comme neuf'), ('0.50' , 'Peu usé'), ('0.25', 'Très usé'), )
	etat = models.CharField(max_length=4,choices=etat_choix, default = '0.75')
	#s'il est reçu 
	recu_choix = (('0' , 'Avec le vendeur'), ('0.25' , 'À la coopérative'), ('0.50' , 'Réservé'), ('0.75' , 'Acheté'), ('1' , "Délivré à l'acheteur"),)
	recu = models.CharField(max_length=4,choices=etat_choix, default = '0')
	
	def __str__(self):
		if self.acheteur!="":
			return str(self.user) +" : "+ self.titre + " de " + self.auteur + " au prix neuf de " + str(self.prix_neuf) + " $" + ", " + dict(self.etat_choix)[self.etat] + ". " + dict(self.recu_choix)[self.recu] + " par " + self.acheteur
		return str(self.user) +" : "+ self.titre + " de " + self.auteur + " au prix neuf de " + str(self.prix_neuf) + " $" + ", " + dict(self.etat_choix)[self.etat] + ". " + dict(self.recu_choix)[self.recu]
	def reserver(self, acheteur):
		self.recu="0.50"
		self.acheteur = str(acheteur)
		self.save()
	def acheter(self,acheteur):
		self.acheteur = str(acheteur)
		self.recu="0.75"
		self.save()
	def remettre(self):
		self.recu = "0.25"
		self.save()
	def supprimer(self):
		self.delete()
	def dupliquer(self):
		n_livre = Livre.objects.get(id=self.id)
		n_livre.id = None
		n_livre.save()

class Argent(models.Model):
	montant = models.CharField(max_length=120, blank=True, null=True)
	username = models.CharField(max_length=120, blank=True, null=True)
	
	def __str__(self):
		return self.username + " a " + self.montant + "$"
		
	
	@staticmethod
	def creer_bourse(username, montant):
		n = Argent(montant=montant,username=username)
		n.save()
	
	def debourser(self, montant):
		self.montant = str(float(self.montant) - float(montant))
		self.save()
		
	def gagner(self, montant):
		self.montant = str(float(self.montant) + float(montant))
		self.save()