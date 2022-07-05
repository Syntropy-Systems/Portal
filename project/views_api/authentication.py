from django.shortcuts import render
from ..serializers.credentials import CredentialSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer


class ObtainAuthToken(APIView):
	throttle_classes = ()
	permission_classes = ()
	parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
	renderer_classes = (renderers.JSONRenderer,)
	serializer_class = AuthTokenSerializer

	def post(self, request, *args, **kwargs):
		post_data = request.data
		from_local_server = post_data.get("from_local_server", False)

		serializer = self.serializer_class(data=post_data)
		if serializer.is_valid():
			user = serializer.validated_data['user']
			if User_roles.objects.filter(user=user, user_rights__name="chrome_app", value=True).exists():
				token, created = Token.objects.get_or_create(user=user)
				to_response = {
					'token': token.key,
					'user_logged': token.user.fullname,
					'company_name': token.user.company.name,
					'company_id': token.user.company.pk,
					# To be transferred to Update Employees/Data
					'emp_id_digits': token.user.company.emp_id_digits
				}
				if from_local_server:
					to_response["user_obj"] = {
						"id": token.user.pk,
						"email": token.user.email,
						"fullname": token.user.fullname
					}
					to_response["company_obj"] = {
						"id": token.user.company.pk,
						"name": token.user.company.name
					}


				return Response(to_response)
			else: return Response("This account don't have mobile/chrome app rights", status=status.HTTP_400_BAD_REQUEST)
		else:
			# Refactor
			print(serializer.errors)
			return Response("Invalid username/password", status=status.HTTP_400_BAD_REQUEST)
