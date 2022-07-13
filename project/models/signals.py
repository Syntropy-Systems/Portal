from project.models.users import *
from project.models.email import *
from django.db.models.signals import post_save

email_instance = Send_email()
def on_user_save(sender,**kwargs):
	is_created = kwargs.get("created",True)
	if is_created:
		instance = kwargs["instance"]
		email_instance.new_client_notification(instance)

post_save.connect(on_user_save, sender = User)
