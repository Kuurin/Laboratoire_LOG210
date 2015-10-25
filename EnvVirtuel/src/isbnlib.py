import re
import urllib.request
from bs4 import BeautifulSoup #http://www.crummy.com/software/BeautifulSoup/

def get_html(url):
	"""Grab html code of a page given its URL"""
	try:
		with urllib.request.urlopen(url) as response:
			html = response.read()
		return html
	except:
		return "error"
		
def get_url_livre(isbn):
	#retourne le url de la page amazon du livre
	url = "http://www.amazon.ca/s/ref=nb_sb_noss?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&url=search-alias%3Dstripbooks&field-keywords=" + str(isbn)
	html = get_html(url)
	soup = BeautifulSoup(html, 'html.parser')
	for link in soup.find_all('a',{ "class" : "a-link-normal s-access-detail-page  a-text-normal" }):
		url = link.get('href')
		break
	return url
		
def get_titre(isbn):
	try:
		html = get_html(get_url_livre(isbn))
		soup = BeautifulSoup(html, 'html.parser')
		titre = soup.find(id="productTitle").string
	except:
		titre = " "
	return str(titre)
	
	
def get_auteur(isbn):
	try :
		html = get_html(get_url_livre(isbn))
		soup = BeautifulSoup(html, 'html.parser')
		auteur = " "
		for span in soup.find_all('span',{ "class" : "author notFaded" }):
			for link in span.find_all('a'):
				auteur = link.string
				break
	
	except: 
		auteur = " "
	#for link in soup.find_all('span',{ "class" : "a-size-small a-color-base" }):
	#	if compteur is 5 :
	#		auteur = link.string
	#		break
	#	compteur = compteur + 1
	return str(auteur)

def get_pages(isbn):
	try:
		html = get_html(get_url_livre(isbn))
		soup = BeautifulSoup(html, 'html.parser')
		pages = " "
		for td in soup.find_all('td', {"class" : "bucket"}):
			for li in td.find_all('li'):
				li = str(li)
				debut = li.find("</b> ") + len("</b> ")
				fin = li.find(" pages")
				pages = li[debut:fin]
				break
		if not pages.isnumeric():
			pages = " "
	except:
		pages = " "
	#soup_string = str(soup)
	#debut = 0
	#fin = 1
	#if soup_string.find(" pages") > 0:
	#debut = soup_string.find("<li><b>Paperback:</b>") + len("<li><b>Paperback:</b>")
	#if soup_string.find(" pages</li>") > 0:
	#	fin = soup_string.find(" pages</li>")
	#pages = " "
	#pages = soup_string[debut:fin]

	return str(pages)

def get_prix(isbn):
	try:
		html = get_html(get_url_livre(isbn))
		soup = BeautifulSoup(html, 'html.parser')
		prix = " "
		classe = "a-color-price"
		for span in soup.find_all('span', {"class": classe}):
			prix = span.string
			break
		nprix = ""
		for char in prix:
			if char.isnumeric() or char is "." or char is ",":
				nprix = nprix + str(char)
		prix = nprix
	except :
		prix = " "
	#classe = "a-size-medium a-color-price offer-price a-text-normal"
	#for span in soup.find_all('span',{ "class" : classe }):
	#	prix = span.string[5:len(span.string)]
	#	break
	return str(prix)
		
if __name__ == "__main__":
	
	isbn = 2012010679
	isbn = 2070375161
	isbn = 9782070368228
	isbn = "284205301X"
	isbn = "1101898283"
	isbn = "0310941784"
	isbn = "0781444993"
	isbn = "0131489062"
	isbn = "978-1101898437"
	isbn = '12093498567'

	print('auteur : ' + get_auteur(isbn))
	print('pages : ' + get_pages(isbn))
	print('prix : ' + get_prix(isbn))
	print('titre : ' + get_titre(isbn))
	