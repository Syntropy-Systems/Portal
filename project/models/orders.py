from django.db import models
from project.views.common import *
from project.models.common import *

class Order(models.Model):
	client = models.ForeignKey("User",related_name = "Own_by",on_delete = models.PROTECT)
	date = models.DateField(null = True)

	available_capacity = models.FloatField(null = True,blank = True)
	capacity = models.FloatField(null = True,blank = True)

	is_deleted = models.BooleanField(default = False)

	class Meta:
		app_label = "project"
		db_table  = "orders"

	def __str__(self):
		return self.client

	def as_dict(self,display = False,billing = False):
		row = model_to_dict(self)
		row["client"] = self.client.as_dict()
		return row

	def get_top_sites(self):
		instances = TopSite.objects.filter(order = self.pk)
		rows = []

		for instance in instances:
			rows.append(instance.as_dict())

		return rows


class TopSite(models.Model):
	order = models.ForeignKey("Order",on_delete = models.PROTECT)
	title = models.TextField()
	url = models.TextField()

	class Meta:
		app_label = "project"
		db_table  = "top_sites"

	def __str__(self):
		return self.client

	def as_dict(self):
		row = model_to_dict(self,fields = [
			"title",
			"url"
		])

		return row