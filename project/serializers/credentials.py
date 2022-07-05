from rest_framework import serializers
from ..models.miscellaneous import Credential

class CredentialSerializer(serializers.ModelSerializer):

	class Meta:
		model = Credential
		fields = (
			"id",
			"name",
			"username",
			"password",
			"url",
			"remarks",
		)