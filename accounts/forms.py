from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from phonenumber_field.formfields import PhoneNumberField

from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget, PhoneNumberPrefixWidget
from accounts.models import User


class RegistrationForm(UserCreationForm):
	email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')
	phone = PhoneNumberField(widget=PhoneNumberPrefixWidget(initial='IQ'))
	phone.error_messages['invalid'] = 'Enter a valid phone number (e.g. +9647801000000).'
	class Meta:
		model = User
		fields = ('email', 'username','firstname','lastname','phone', 'password1', 'password2', )
# 		error_messages = {
#             'phone' : {
#                 'required' : _("Enter a valid phone number (e.g. +9647801000000).")
#             }
#         }


class UserAuthenticationForm(forms.ModelForm):

	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('email', 'password')

	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Invalid login")


class UserUpdateForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ('email', 'username','firstname','lastname','phone' )

	def clean_email(self):
		email = self.cleaned_data['email']
		try:
			User = User.objects.exclude(pk=self.instance.pk).get(email=email)
		except User.DoesNotExist:
			return email
		raise forms.ValidationError('Email "%s" is already in use.' % User)

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			User = User.objects.exclude(pk=self.instance.pk).get(username=username)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError('Username "%s" is already in use.' % username)
