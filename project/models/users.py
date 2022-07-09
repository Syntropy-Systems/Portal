from django.db import models
from django.contrib.auth import hashers
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.postgres.fields import JSONField,ArrayField
from project.views.common import *

class User_Manager(BaseUserManager):

	def create_user2(self, email, password):
		user = self.model(email = email, password = password)
		return user

	def create_superuser2(self, email, password):
		user.save()
		return user

	
	def _create_user(self, email, password,superadmin,**extra_fields):
		"""
		Creates and saves a User with the given email and password.
		"""
		if not email:
			raise ValueError('The given email must be set')
		
		user = self.model(email = email, password = password,is_staff = True,is_developer = True,fullname = "Developer")
		user.set_password(password)
		user.save()
		return user

	# def create_user(self, email, password=None, **extra_fields):
	# 	return self._create_user(email, password,False)

	def create_superuser(self, email, password, **extra_fields):
		return self._create_user(email, password,True)

class User(AbstractBaseUser):
	email = models.EmailField(max_length = 254, null = False, blank = False, unique = True)

	firstname = models.TextField()
	lastname = models.TextField()
	fullname = models.CharField(max_length = 50, null = False, blank = False)

	address = models.TextField(null = True,blank = True)

	gender = models.CharField(max_length = 50, null = False, blank = False)
	other_gender = models.CharField(max_length = 50, null = True, blank = True)


	birthdate = models.DateField()

	ethnicity_race = models.CharField(max_length = 50)
	ethnicity_hispanic_origin = models.BooleanField(default=False)

	occupation = models.CharField(max_length = 50, null = False, blank = False)

	is_active = models.BooleanField(default = True)
	created_on = models.DateTimeField(auto_now_add = True)

	#Must have fields for Admin
	is_staff = models.BooleanField(default=False)
	is_developer = models.BooleanField(default=False)
	is_employee = models.BooleanField(default=False)

	USERNAME_FIELD = 'email'
	objects = User_Manager()

	class Meta:
		app_label = "project"
		db_table = "User"
		ordering = ["email"]

	def __str__(self):
		return self.fullname

	def __init__(self, *args, **kwargs):
		super(User, self).__init__(*args, **kwargs)
		if self.password:
			self._old_password = self.password
		else:
			self._old_password = None

	def as_dict(self):
		return {
			"id": self.pk,
			"email": self.email,
			"fullname": self.fullname,
			"address": self.address,
			"is_active": self.is_active,
		}

	def save(self, *args, **kwargs):
		if self._old_password is None or self._old_password != self.password:
			if "pbkdf2_sha256" not in self.password:
				self.password = hashers.make_password(self.password)

		super(User, self).save(*args, **kwargs)

	def delete(self, deleted_by = None,delete_forever = False):
		self.is_active = False
		self.save()

	def is_superuser(self):
		return self.is_developer


	@property
	def is_cda(self):
		return self.user_type.name == "CDA"

	@property
	def is_admin(self):
		return self.user_type.name == "Admin"

	@property
	def is_client(self):
		return self.user_type.name == "Client"

	def has_perm(self, perm, obj=None):
		return self.is_developer

	def has_module_perms(self, app_label):
		return self.is_developer


	def get_full_name(self): 
		return self.fullname

	def get_short_name(self):
		return self.get_full_name()
		
	def get_absolute_url(self):
		return "/user/%s/" % urlquote(self.email)

	