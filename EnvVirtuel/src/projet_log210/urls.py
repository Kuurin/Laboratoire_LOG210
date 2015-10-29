
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    url(r'^$', 'cooperative.views.home', name='home'),
	url(r'^optionsetudiant/', 'cooperative.views.optionsetudiant', ),
	url(r'^optionsgestionnaire/', 'cooperative.views.optionsgestionnaire', ),
	
    url(r'^admin/', include(admin.site.urls)),
	url(r'^registercoop/', 'cooperative.views.registercoop',),
	
	#login
	url(r'^login/', 'django.contrib.auth.views.login',{'template_name': 'login.html'}),
	url(r'^logout/', 'django.contrib.auth.views.logout',{'next_page': '/'}),
	url(r'^registergestionnaire/', 'cooperative.views.register_user_gestionnaire',),
	url(r'^registeretudiant/', 'cooperative.views.register_user_etudiant',),
	url(r'^register_success/', 'cooperative.views.register_success',),
	
	url(r'^ajouterlivre/', 'cooperative.views.ajouterlivre',),
	url(r'^ajouterlivredescription/', 'cooperative.views.ajouterlivredescription',),
	url(r'^etudiantvoirlivres/', 'cooperative.views.etudiantvoirlivres',),
	url(r'^etudiantvoirofferts/', 'cooperative.views.etudiantvoirofferts',),
	url(r'^etudiantvoirreserves/', 'cooperative.views.etudiantvoirreserves',),
#	url(r'^etudiantvoirarecuperer/', 'cooperative.views.etudiantvoirreserves',),
	
	

	url(r'^recherche/', 'cooperative.views.recherche'),
	url(r'^gestionnairevoirlivres/', 'cooperative.views.gestionnairevoirlivres'),
	url(r'^gestionnairerecus/', 'cooperative.views.gestionnairerecus'),
	url(r'^actionlivre/', 'cooperative.views.actionlivre'),
	url(r'^modifierlivre/', 'cooperative.views.modifierlivre'),
	
	
	
	
	
	]
