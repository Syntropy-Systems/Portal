from project.views.common import *
from project.models.users import User

recipients = ["weprobpo@gmail.com",]


class Send_email(models.Model):
	recipients = ["aldesabido@gmail.com",]

	def new_client_notification(self,instance):
		template_url = "email_templates/new_client.tpl"

		params = {} 
		params['subject'] = "[New Account] Syntropy account confirmation" 
		params['email'] = instance.email 
		params['name'] = instance.fullname 
		params['message'] = "To verify your account, kindly click the link below." 




		token = str_base64_encode(str(instance.pk))
		token = urlsafe_base64_encode(token)


		url = "/activate_account/%s/"%(token) 
		base_url = "http://localhost:8000" 
		base_url = "https://oyster-app-m35t8.ondigitalocean.app" 

		params['url'] = base_url+url

		recipients = ["aldesabido@gmail.com"]
		if settings.ENVIRONMENT != "production":
			bccs = []  
			recipients = ["aldesabido@gmail.com",]  

		# instance.activate_token = token
		# super(User, instance).save()

		send_mail(template_url,params,"Syntropy <aldesabido@gmail.com>",recipients)