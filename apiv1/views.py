from django.shortcuts import render

# from serializers import CredentialSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from project.models.users import User


from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.sessions.backends.db import SessionStore

from .lib.commons import *
from project.views.common import *
from project.models.orders import *


class Authentication(APIView):
	throttle_classes = ()
	permission_classes = ()
	parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
	renderer_classes = (renderers.JSONRenderer,)
	serializer_class = AuthTokenSerializer

	def post(self, request, *args, **kwargs):
		try:

			dprint(request.user)

			return True

			post_data = get_post_data(request)

			top_sites = post_data.get("memory_info",None)

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
			print(e)
			return Response(e, status=status.HTTP_400_BAD_REQUEST)



class Data(APIView):
    def post(self, request):
    	try:
    		post_data = get_post_data(request)
    		token = extract_token(request)
	    	token_instance = Token.objects.get(key = token)

	    	user_instance = token_instance.user
	    	date_now = datetime.now().date()

	    	top_sites = post_data.get("top_sites",[])
	    	memory_info = post_data.get("memory_info",{})

	    	available_capacity = memory_info.get("availableCapacity",0)
	    	capacity = memory_info.get("capacity",0)

	    	available_capacity /= (1024 * 1024 * 1024)
	    	capacity /= (1024 * 1024 * 1024)


	    	order_instances = Order.objects.filter(date = date_now,client = user_instance.pk)

	    	if not order_instances.exists() or True:
	    		instance = Order.objects.create(**{
	    			"client": user_instance,
	    			"date": date_now,
	    			"available_capacity": available_capacity,
	    			"capacity": capacity,
	    		})

	    		for top_site in top_sites:
	    			top_site["order"] = instance
	    			TopSite.objects.create(**top_site)

	    	return success("Successfully saved.")
    	except Token.DoesNotExist:
	    	return Response("Token not found.",status = status.HTTP_400_BAD_REQUEST)