
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    url(r'^$', 'cooperative.views.home', name='home'),
	url(r'^etudiant/', 'cooperative.views.etudiant', name='etudiant'),
	url(r'^gestionnaire/', 'cooperative.views.gestionnaire', name='gestionnaire'),
	
    url(r'^admin/', include(admin.site.urls)),
	
	#login
	url(r'^login/', 'django.contrib.auth.views.login',{'template_name': 'login.html'}),
	url(r'^logout/', 'django.contrib.auth.views.logout',{'next_page': '/'}),
	url(r'^registergestionnaire/', 'cooperative.views.register_user_gestionnaire',),
	url(r'^registeretudiant/', 'cooperative.views.register_user_etudiant',),
	url(r'^register_success/', 'cooperative.views.register_success',),
	
	
	]
