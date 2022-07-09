from django import forms
from ..models.users import *


class Users_create_form(forms.ModelForm):
	class Meta:
		model = User
		fields = (
			'email',
			'firstname',
			'lastname',
			'fullname',
			'address',
			'gender',
			'other_gender',
			'birthdate',
			'ethnicity_race',
			'ethnicity_hispanic_origin',
			'occupation',
			'password',
		)