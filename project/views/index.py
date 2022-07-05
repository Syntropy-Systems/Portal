from ..forms.users import *
from ..models.users import *
from ..views.common import *

from django.contrib.auth import authenticate, hashers, logout as logoutt, login as loginn
from django.contrib.auth.tokens import default_token_generator 
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode 



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

def register(request):
	try: 
		params = post_data(request)
		user_type = params.get("user_type","client")

		user_type = User_type.objects.get(code__iexact= user_type)
		params["user_type"] = user_type.pk

		if "is_bpo" in params or "is_va" in params:
			if not params.get("is_bpo",False) and not params.get("is_va",False):
				raise_error("You need to select atleast one service type.")

		if not params.get("is_bpo",False) and not params.get("is_va",False):
			params["is_bpo"] = True

		try:
			instance = User.objects.get(id = params.get("id",None))
			params["is_va"] = instance.is_va
			params["is_bpo"] = instance.is_bpo
			user_form = Users_edit_form(params,instance = instance)
			editing = True
		except Exception as e:
			user_form = Users_create_form(params)
			editing = False

		if user_form.is_valid():
			user_save = user_form.save()
			
			if not editing:
				user_save.is_active = True
				user_save.save()

			print("%s - %s"%(user_save.is_bpo,user_save.is_va))
			return success()
		else:
			raise_error(user_form.errors,True)

	except Exception as err:
		return error(err)

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
					raise ValueError("This user is inactive. Kindly contact your admin at weprobpo@gmail.com")
				loginn(request, user)
				return success("Successfully logged in. Redirecting...")
			else:
				raise_error("Invalid username/password.")
		except Exception as e:
			return error(e)
	else:
		return redirect("loginpage")

@require_GET
def logout(request):
	request.session.clear()
	logoutt(request)
	return redirect("loginpage")

#BPO
@require_GET
def home(request):
	user_instance = request.user
	return render(request, 'base.html')

def dashboard(request):
	if request.method == "GET":
		return render(request, 'home/dashboard.html')

def orders(request):
	if request.method == "GET":
		return render(request, 'orders/active.html')