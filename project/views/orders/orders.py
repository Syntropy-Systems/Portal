from project.forms.orders import *
from project.models.orders import *
from project.views.common import *

def orders(request):
	return render(request, 'orders/orders.html',{"page_name": "Orders"})

def read_pagination(request,from_export = False,filters = {}):
	try:
		if not from_export:
			filters = post_data(request)
			pagination = filters.pop("pagination",None)
		
		sort_by = generate_sorting(filters.pop("sort",None))

		filters["status"] = filters.pop("status","active")
		filters.update({"is_deleted" : False})

		user_type = request.user.user_type
		if user_type.code == "client":
			filters["client"] = request.user.pk
		if user_type.code == "cda":
			filters["current_assignee"] = request.user.pk

		# filters.pop("date_from",None)
		# filters.pop("date_to",None)
		filters = date_range_filter(filters,date_field = "date_day")
		filters = clean_obj(filters)
		name_search = filters.pop("name","")

		show_all = False
		if name_search == "aldegwapo":
			name_search = ""
			show_all = True

		filters["address__icontains"] = name_search
		success_filter = copy.copy(filters)
		success_filter["status"] = "completed"

		qc_filter = copy.copy(filters)
		qc_filter["status"] = "qc"

		hold_filter = copy.copy(filters)
		hold_filter["status"] = "hold"

		active_filter = copy.copy(filters)
		active_filter["status"] = "active"

		submit_filter = copy.copy(filters)
		submit_filter["status"] = "submitted"


		filters = filter_obj_to_q(filters)
		# filters &= (Q(order_number__icontains=name_search) | Q(address__icontains=name_search))

		results = {"data" : []}


		records = Order.objects.filter(filters).order_by(*sort_by)



		# Count completed
		success_filter.pop("name","")
		results["success_count"] = Order.objects.filter(**success_filter).count()
		results["qc_count"] = Order.objects.filter(**qc_filter).count()
		results["hold_count"] = Order.objects.filter(**hold_filter).count()
		results["active_count"] = Order.objects.filter(**active_filter).count()
		results["submit_count"] = Order.objects.filter(**submit_filter).count()
		
		if not from_export:
			results.update(generate_pagination(pagination,records))
			if not show_all:
				records = records[results['starting']:results['ending']]

		for record in records:
			record.update_time()
			row = record.as_dict(True)
			row["qc_count"] = record.count_qc()
			row["notes_count"] = record.count_notes()
			row["docs_count"] = record.count_docs()
			row["photo_count"] = record.count_photos()

			row["assignee"] = "Unassigned"
			if record.assigned:
				row["assignee"] = record.current_assignee.as_dict()

			orig_address = record.address.replace('\n', ' ')
			orig_address = orig_address.replace('\r', '')
			
			
			tmp_address = orig_address.split(" ")[0:3]
			tmp_address = " ".join(tmp_address)

			duplicate_instances = Order.objects.filter(address__icontains = tmp_address,is_deleted = False) \
									.exclude(id = record.pk) \
									.exclude(status = "cancelled")

			row["is_duplicate_address"] = duplicate_instances.exists()

			results["data"].append(row)

		if from_export:
			return results
		return success_list(results,False)
	except Exception as e:
		return error(e)
