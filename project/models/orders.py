from django.db import models
from project.views.common import *
from project.models.common import *

class Order(models.Model):
	client = models.ForeignKey("User",related_name = "Own_by")
	date = models.DateField(null = True)
	is_deleted = models.BooleanField(default = False)

	class Meta:
		app_label = "project"
		db_table  = "orders"

	def __str__(self):
		return self.client

	def delete(self,hard_delete = False):
		if hard_delete:
			super(Order, self).delete()
		else:
			self.is_deleted = True
			self.save()

	def save(self):
		super(Order, self).save()

	def as_dict(self,display = False,billing = False):
		row = model_to_dict(self,fields = [
			"id",
			"date",
		])

		if display:
			row["client"] = self.client.get_full_name()
		else:
			row["client"] = self.client.as_dict()

		row["date"] = self.date.date()
		return row

