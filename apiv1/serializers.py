from rest_framework import serializers
from project.models.miscellaneous import Test_class,Credential



class CredentialSerializer(serializers.ModelSerializer):
	class Meta:
		model = Credential
		fields = (
			"id",
			"name","username",
			"password",
			"url",
			"remarks"
		)




