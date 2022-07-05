from django.shortcuts import render
from ..serializers.credentials import CredentialSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class CredentialView(APIView):
	serializer_class = CredentialSerializer

	def get_queryset(self):
		user_id = self.kwargs['user_id']
		return Credential.objects.filter(user=user_id,is_deleted = False).order_by("name")