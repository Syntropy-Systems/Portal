
from django.conf.urls import url, handler404,include

from project.views_api import (
		credentials,
	)


urlpatterns = [
	url(r'', credentials.CredentialView.as_view()),
	url(r'^login', credentials.CredentialView.as_view()),
	url(r'^credentials', credentials.CredentialView.as_view()),
]
