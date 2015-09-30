
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    url(r'^$', 'cooperative.views.home', name='home'),
	url(r'^etudiant/', 'cooperative.views.etudiant', name='etudiant'),
	url(r'^gestionnaire/', 'cooperative.views.gestionnaire', name='gestionnaire'),
	
    url(r'^admin/', include(admin.site.urls)),
]