import requests
from bs4 import BeautifulSoup #http://www.crummy.com/software/BeautifulSoup/

def get_html(num):
	url = "http://www.freesmsgateway.info/"
	r = requests.post(url, data={'phonenum':num,'error':'true','x':'0','y':'0'})
	html = r.text
	return html
	
		
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
		if not "@" in email:
			#l'adresse par défaut en cas d'erreur
			return "4383908982@fido.ca"
		return email
	except:
		return ""


		
if __name__ == "__main__":
	num = "5149655579"
	get_email(num)