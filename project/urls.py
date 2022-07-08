
from django.conf.urls import url, handler404,include
from django.conf import settings as root_settings
from django.conf.urls.static import static

from project.views import (
		index,
		common,
		common_requests,
		users,
	)

from project.views.orders import (
		orders
	)


urlpatterns = [
	url(r'^$', index.landingpage,name="landingpage"),
	url(r'^login/$', index.loginpage,name="loginpage"),
	url(r'^login/submit/$', index.login),
	url(r'^logout/$', index.logout),
	url(r'^register/create_dialog/$', index.registration_dialog),
	url(r'^register/$', index.register),
	url(r'^user_update/$', index.register),


	#Common Requests & Common templates
	url(r'^common/pagination/$', common_requests.pagination),


	url(r'^home/$', index.home,name="home"),
	url(r'^dashboard/$', index.dashboard),
	
	#Orders
	url(r'^orders/$', orders.orders),
	url(r'^orders/read_pagination/$', orders.read_pagination),
	url(r'^orders/export/$', orders.export),
	
	#Settings
	url(r'^users/$', users.home),
	url(r'^users/create_dialog/$', users.create_dialog),
	url(r'^users/change_password_dialog/$', users.change_password_dialog),
	url(r'^users/change_password/$', users.change_password),
	url(r'^users/read_pagination/$', users.read_pagination),
	url(r'^users/load_to_edit/(?P<pid>[0-9]+)$$', users.load_to_edit),
	url(r'^users/delete/(?P<pid>[0-9]+)/$', users.delete),
]
# urlpatterns += static(root_settings.STATIC_URL,document_root=root_settings.STATIC_ROOT)
# urlpatterns += static(root_settings.MEDIA_URL,document_root=root_settings.MEDIA_ROOT)

# if root_settings.DEBUG:
#     import debug_toolbar
#     urlpatterns.append(url(r'^__debug__/', include(debug_toolbar.urls)))