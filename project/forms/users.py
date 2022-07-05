from django import forms
from ..models.users import *


class Users_create_form(forms.ModelForm):
	class Meta:
		model = User
		fields = (
			'email',
			'fullname',
			'address',
			'contact_no',
			'password',
		)
