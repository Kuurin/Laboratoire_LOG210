import requests
from bs4 import BeautifulSoup #http://www.crummy.com/software/BeautifulSoup/

def get_html(num):
	url = "http://www.freesmsgateway.info/"
	r = requests.post(url, data={'phonenum':num,'error':'true','x':'0','y':'0'})
	html = r.text
	#print(html + "...")
	return html
	
		
def get_url_livre(isbn):
	#retourne le url de la page amazon du livre
	url = "http://www.amazon.ca/s/ref=nb_sb_noss?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&url=search-alias%3Dstripbooks&field-keywords=" + str(isbn)
	html = get_html(url)
	soup = BeautifulSoup(html, 'html.parser')
	for link in soup.find_all('a',{ "class" : "a-link-normal s-access-detail-page  a-text-normal" }):
		url = link.get('href')
		break
	return url
		
def get_email(num):
	try:
		html = get_html(num)
		soup = BeautifulSoup(html, 'html.parser')
		soup_string = str(soup)
		debut = 0
		fin = 1
		if soup_string.find("SMS Gateway Address: ") > 0:
			debut = soup_string.find("SMS Gateway Address: ") + len("SMS Gateway Address: ")
		if soup_string.find("MMS Gateway Address: ") > 0:
			fin = soup_string.find("MMS Gateway Address: ")-15
		email = " "
		email = soup_string[debut:fin]
		return email
	except:
		return ""


		
if __name__ == "__main__":
	num = "5149655579"
	get_email(num)