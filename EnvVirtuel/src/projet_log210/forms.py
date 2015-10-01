from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class EtudiantRegistrationForm(UserCreationForm):
	email = forms.EmailField(required=True)
	phone = forms.CharField()
	
	class Meta:
		model = User
		fields = ('username', 'email', 'phone', 'password1', 'password2')
	
	#validation phone number	
	def clean_phone(self):
		value = self.cleaned_data['phone']
		for char in value:
			if not char.isdigit():
				char.remove()
		if len(value) is not 10:
			raise forms.ValidationError("Votre numéro doit être écrit avec 10 chiffres")
		return value
		
		
	
	def save(self,  commit=True):
		user = super(EtudiantRegistrationForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		user.phone = self.cleaned_data['phone']
		
		if commit:
			user.save()
			
		return user

		