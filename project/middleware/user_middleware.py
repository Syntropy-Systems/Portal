from django.shortcuts import redirect
from ..views.common import *
import json
from django.utils.deprecation import MiddlewareMixin

class UserMiddleware(MiddlewareMixin):
	"""Checks if the user is allowed to access the page they are requesting."""

	def process_request(self, request):
		"""The main part of the middleware, called each time a user makes a request."""
		# Initialization.
		url = request.path
		urls = url.replace("//", "/").split("/")
		first_url = urls[1]

		if 'HTTP_AUTHORIZATION' in request.META or "api" in first_url:
			return None
		

		if first_url == 'superradmin':
			return None

		not_required_session = [
			"register",
			"login",
			"logout",
			"landingpage",
		]

		no_action = [
			"logout",
			"",
			"/",
			# "apiv1",
		]

		if first_url not in not_required_session and not request.user.id:
			if request.method == "GET":
				if first_url not in no_action:
					return redirect("loginpage")

		if first_url in not_required_session and request.user.id:
			if request.method == "GET":
				if first_url not in no_action:
					return redirect("home")

		return None


