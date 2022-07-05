from django import forms
from ..models.orders import *


class Order_create_form(forms.ModelForm):
	class Meta:
		model = Order
		fields = (
			'client',
			'date',
			'is_deleted',
	)
