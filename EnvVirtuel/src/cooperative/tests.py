from django.test import TestCase
from cooperative.models import *

class ArgentTestCase(TestCase):
	def setUp(self):
		Argent.creer_bourse("acheteur","1000")
		Argent.creer_bourse("vendeur","1000")
	
	def test_achat_vente(self):
		Argent.debourser("acheteur","10")
		Argent.gagner("vendeur","10")
		acheteur = Argent.objects.get(username="acheteur")
		vendeur = Argent.objects.get(username="vendeur")
		self.assertEqual(acheteur.montant,"990.00")
		self.assertEqual(vendeur.montant,"1010.00")
    

class LivreTestCase(TestCase):
	def setUp(self):
		Livre.objects.create(user="user1",ISBN="1234567890",titre="Moise",auteur="Ame",nb_pages="10",prix_neuf="50",etat="0.75",recu="0")
		Livre.objects.create(user="user2",ISBN="1234567890",titre="Moise2",auteur="Ame",nb_pages="10",prix_neuf="50",etat="0.75",recu="0")
		Argent.creer_bourse("user1","1000")
		Argent.creer_bourse("user2","1000")
	
	def test_ajout_livre(self):
		print("nombre de livres= " + str(len(Livre.objects.all())))
		self.assertEqual(len(Livre.objects.all()),2)
	def test_dupliquer(self):
		initialLength = len(Livre.objects.all())
		livre = Livre.objects.get(user="user1")
		livre.dupliquer()
		finalLength = len(Livre.objects.all())
		self.assertEqual(initialLength+1,finalLength)
	def test_supprimer(self):
		initialLength = len(Livre.objects.all())
		livre = Livre.objects.get(user="user1")
		livre.dupliquer()
		livre.supprimer()
		finalLength = len(Livre.objects.all())
		self.assertEqual(initialLength,finalLength)
	def test_remettre(self):
		livre = Livre.objects.get(titre="Moise")
		livre.remettre()
	def test_reserver(self):
		livre = Livre.objects.get(user="user1")
		livre.reserver("oli")
		self.assertEqual(livre.recu,"0.50")
		self.assertEqual(livre.acheteur,"oli")
	def test_dereserver(self):
		livre = Livre.objects.get(user="user1")
		livre.reserver("oli")
		livre.dereserver("oli")
		self.assertEqual(livre.recu,"0.25")
		self.assertEqual(livre.acheteur,"")
	def test_acheter(self):
		livre = Livre.objects.get(user="user1")
		montantInitUser2 = float(Argent.objects.get(username="user2").montant)
		livre.acheter("user2")
		self.assertEqual(livre.recu,"0.75")
		self.assertEqual(livre.acheteur,"user2")
		self.assertEqual(float(Argent.objects.get(username="user2").montant),montantInitUser2-(float(livre.etat) * float(livre.prix_neuf)))
	def test_annulertransaction(self):
		livre = Livre.objects.get(user="user1")
		montantInitUser2 = float(Argent.objects.get(username="user2").montant)
		livre.acheter("user2")
		livre.annulertransaction()
		self.assertEqual(livre.acheteur,"")
		self.assertEqual(livre.recu,"0.25")
		self.assertEqual(montantInitUser2,float(Argent.objects.get(username="user2").montant))
	def test_livrer(self):
		livre = Livre.objects.get(user="user1")
		livre.acheter("user2")
		livre.livrer()
		self.assertEqual(livre.recu, "1")
    