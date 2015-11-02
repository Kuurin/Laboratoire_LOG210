from django.db import models
import decimal
import smtplib
import gatewaylib
from DateTime import *
from django.contrib.auth.models import User


class Cooperative(models.Model):
	nom = models.CharField(max_length=120, blank=False, null=True)
	adresse = models.CharField(max_length=1000, blank=False, null=True)
	
	def __str__(self):
		return self.nom
		
class Etudiant(User):
	def __init__(self, *args, **kwargs):
		super(Etudiant, self).__init__(*args, **kwargs)
	
	@staticmethod
	def contacter(username, message):
		#notification par courriel
		#Morceau de code par Alex Le
		#http://alexanderle.com/blog/2011/send-sms-python.html
		#consulé le 29-10-2015, publié le 05-06-2011
		server = smtplib.SMTP( "smtp.gmail.com", 587 )
		server.starttls()
		server.login( 's20153log210eq01@gmail.com', 'serpentard' )
		destination = username
		if not "@" in destination:
			destination = gatewaylib.get_email(destination)
		server.sendmail( 'Cooperative ETS', destination, message )
		
	
		
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
	recu_choix = (('0' , 'Avec le vendeur'), ('0.25' , 'A la cooperative'), ('0.50' , 'Reserve'), ('0.75' , 'Achete'), ('1' , "Delivre à l'acheteur"),)
	recu = models.CharField(max_length=4,choices=recu_choix, default = '0')
	
	def __str__(self):
		if self.acheteur!="":
			return str(self.user) +" : "+ self.titre + " de " + self.auteur + " au prix de " + "%.2f" % round(float(self.etat) * float(self.prix_neuf)) + " $, " + dict(self.etat_choix)[self.etat] + ". " + dict(self.recu_choix)[self.recu] + " par " + self.acheteur
		return str(self.user) +" : "+ self.titre + " de " + self.auteur + " au prix de " + "%.2f" % round(float(self.etat) * float(self.prix_neuf)) + " $, " + dict(self.etat_choix)[self.etat] + ". " + dict(self.recu_choix)[self.recu]
	
	def reserver(self, acheteur):
		self.recu="0.50"
		self.acheteur = str(acheteur)
		self.save()
	def dereserver(self, acheteur):
		self.acheteur=""
		self.recu = "0.25"
		self.save()
	def annulertransaction(self):
		if self.recu == "0.75":
			self.recu="0.25"
			prix = float(self.etat) * float(self.prix_neuf)
			Argent.debourser(self.user, prix)
			Argent.gagner(self.acheteur,prix)
			self.acheteur = ""
			self.save()
	def acheter(self,acheteur):
		self.acheteur = str(acheteur)
		self.recu="0.75"
		prix = float(self.etat) * float(self.prix_neuf)
		Argent.debourser(self.acheteur, prix)
		Argent.gagner(self.user,prix)
		Etudiant.contacter(self.acheteur,"Vous avez achete " + str(self.titre))
		Etudiant.contacter(self.user, "Votre livre a ete achete " + str(self.titre))
		
		self.save()
	def remettre(self):
		if self.recu=="0":
			self.recu = "0.25"
			Etudiant.contacter(self.user, str(self.titre) + " a ete remis a la cooperative")
		self.save()
	def livrer(self):
		if self.recu=="0.75":
			self.recu = "1"
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
		return self.montant + "$"
		
	
	@staticmethod
	def creer_bourse(username, montant):
		n = Argent(montant=montant,username=username)
		n.save()
	@staticmethod
	def debourser(username, montant):
		u = Argent.objects.get(username=username)
		#Morceau de code emprunté à Rex Logan, réponse du 18 janvier 2009
		#http://stackoverflow.com/questions/455612/limiting-floats-to-two-decimal-points
		#Consulé le 29 octobre 2015
		u.montant = "%.2f" % round((float(u.montant) - float(montant)),2)
		u.save()
	@staticmethod	
	def gagner(username, montant):
		u = Argent.objects.get(username=username)
		u.montant = "%.2f" % round((float(u.montant) + float(montant)),2)
		u.save()

