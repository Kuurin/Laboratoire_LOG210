from django.test import TestCase
from cooperative.models import *

class ArgentTestCase(TestCase):
	def setUp(self):
		Argent.objects.create(username="acheteur",montant="1000.00")
		Argent.objects.create(username="vendeur",montant="1000.00")
	
	def test_achat_vente(self):
		Argent.debourser("acheteur","10")
		Argent.gagner("vendeur","10")
		acheteur = Argent.objects.get(username="acheteur")
		vendeur = Argent.objects.get(username="vendeur")
		self.assertEqual(acheteur.montant,"990.00")
		self.assertEqual(vendeur.montant,"1010.00")
    