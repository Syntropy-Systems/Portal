from ..forms.users import *
from ..models.users import *
from ..views.common import *

from django.contrib.auth import authenticate, hashers, logout as logoutt, login as loginn
from django.contrib.auth.tokens import default_token_generator 
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode 

from rest_framework.authtoken.models import Token

def landingpage(request):
	if not request.user.id:
		return redirect("loginpage")
	else:
		return redirect("home")

def loginpage(request):
	if not request.user.id:
		return render(request, 'home/login_page.html')
	else:
		return redirect("home")

def registration_dialog(request):
	return render(request, 'home/dialogs/register.html')

@require_POST
def login(request):
	"""Javascript sends data here. The user is either then authenticated, asked to select a company or errors are returned."""
	if request.method == "POST":
		result = {}
		data = post_data(request)
		try:
			username = data.get('email',"")
			password = data.get('password',"")

			user = authenticate(username = username, password = password)

			if user:
				if not user.is_active:
					raise ValueError("This user is inactive. Kindly contact your admin at aldesabido@gmail.com")

				if not user.activated and not user.is_developer:
					raise ValueError("Your account is still not activated. Kindly check your email to verify.")

				loginn(request, user)

				token, created = Token.objects.get_or_create(user=user)


				response = HttpResponse('Successfully logged in. Redirecting...')
				response.set_cookie('token', token)
				
				return response
				# return success("")
			else:
				raise_error("Invalid username/password.")

		except Exception as e:
			return error(e)
	else:
		return redirect("loginpage")


def register(request):
	try: 
		params = post_data(request)
		params["fullname"] = "%s %s"%(params["firstname"],params["lastname"])

		try:
			instance = User.objects.get(id = params.get("id",None))
			user_form = Users_create_form(params,instance = instance)
		except Exception as e:
			user_form = Users_create_form(params)

		if user_form.is_valid():
			user_save = user_form.save()
			return success()
		else:
			raise_error(user_form.errors,True)

	except Exception as err:
		print(err)
		return error(err)

@require_GET
def activate_account(request,token): 
	data = {
		"message_data":{
			"message": "Account successfully activated. You can now signin using your account.",
			"type": "success",
		}
	}

	try:

		uid = str_base64_decode(urlsafe_base64_decode(token))
		uid = int(uid)

		try: 
			user = User.objects.get(pk=uid) 
		except User.DoesNotExist: 
			raise_error("Confirmation code not found.")

		if user.activated:
			raise_error("This account is already active.")

		user.is_active = True
		user.activated = True
		user.save() 
		return render(request, 'activate_successful.html',data)

	except Exception as e: 
		return error(e)

		e = str(e)
		data["message_data"]["message"] = e
		data["message_data"]["type"] = "error"
		return render(request, 'accounting/landing_page/login_page.html',data)




@require_GET
def logout(request):
	# response = HttpResponse('Successfully logged out. Redirecting...')

	request.session.clear()
	logoutt(request)

	response = redirect("loginpage")
	response.delete_cookie('token')
	
	return response

#BPO
@require_GET
def home(request):
	user_instance = request.user
	return render(request, 'base.html')

def dashboard(request):
	if request.method == "GET":
		return render(request, 'home/dashboard.html')