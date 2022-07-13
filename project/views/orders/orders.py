from project.forms.orders import *
from project.models.orders import *
from project.views.common import *

def orders(request):
	return render(request, 'orders/orders.html',{"page_name": "Title Here!"})

def read_pagination(request,from_export = False,filters = {}):
	try:
		if not from_export:
			filters = post_data(request)
			pagination = filters.pop("pagination",None)
		
		user_instance = request.user
		sort_by = generate_sorting(filters.pop("sort",None))

		status = filters.pop("status",None)
		filters.update({"is_deleted" : False})

		name_search = filters.pop("name","")

		if name_search:
			filters["client__fullname__icontains"] = name_search

		results = {"data" : []}
		records = Order.objects.filter(**filters) \
						.select_related("client") \
						.order_by(*sort_by)


		if not user_instance.is_developer:
			records = records.filter(client = user_instance.pk)

		if not from_export:
			results.update(generate_pagination(pagination,records))
			records = records[results['starting']:results['ending']]

		for record in records:

			row = record.as_dict()

			row["available_capacity"] = round(row["available_capacity"],2)
			row["capacity"] = round(row["capacity"],2)
			
			user_dict = row.get("client")
			if user_dict.get("occupation") == "in_person":
				row["client"]["occupation"] = "In Person"
			elif user_dict.get("occupation") == "remote":
				row["client"]["occupation"] = "Remote"
			else:
				row["client"]["occupation"] = "Hybrid"

			
			row["client"]["ethnicity_hispanic_origin"] = "Yes" if user_dict.get("ethnicity_hispanic_origin") else "No"
			row["top_sites"] = record.get_top_sites()

			results["data"].append(row)


		if from_export:
			return results

		return success_list(results,False)
	except Exception as e:
		print(e)
		return error(e)

def export(request):
	try:
		filters = json.loads(request.GET.get("filters", "{}"))

		response = read_pagination(request,from_export = True,filters = filters)
		records = response["data"]

		output = io.BytesIO() 
		workbook = xlsxwriter.Workbook(output) 
		worksheet = workbook.add_worksheet() 

		row = 0
		worksheet.write(row,0,"Date",get_format(workbook,*["bold"])) 
		worksheet.set_column(0,0,15) 
		worksheet.write(row,1,"Client",get_format(workbook,*["bold"])) 
		worksheet.set_column(1,1,25) 

		worksheet.write(row,2,"Address",get_format(workbook,*["bold"])) 
		worksheet.set_column(2,2,25) 

		worksheet.write(row,3,"Gender",get_format(workbook,*["bold"])) 
		worksheet.set_column(3,3,15) 

		worksheet.write(row,4,"Race",get_format(workbook,*["bold"])) 
		worksheet.set_column(4,4,15) 

		worksheet.write(row,5,"Hispanic Origin",get_format(workbook,*["bold"])) 
		worksheet.set_column(5,5,15) 

		worksheet.write(row,6,"Occupation",get_format(workbook,*["bold"])) 
		worksheet.set_column(6,6,15) 

		worksheet.write(row,7,"Birthdate",get_format(workbook,*["bold"])) 
		worksheet.set_column(7,7,15) 


		worksheet.write(row,8,"Available Capacity",get_format(workbook,*["bold"])) 
		worksheet.set_column(8,8,15) 
		worksheet.write(row,9,"Capacity",get_format(workbook,*["bold"])) 
		worksheet.set_column(9,9,15) 
		worksheet.write(row,10,"Site Name",get_format(workbook,*["bold"])) 
		worksheet.set_column(10,10,30) 
		worksheet.write(row,11,"Site URL",get_format(workbook,*["bold"])) 
		worksheet.set_column(11,11,30) 

		for record in records:
			row += 1 

			date = str(date_to_str(record["date"],format = "%m/%d/%Y"))
			birthdate = str(date_to_str(record["client"]["birthdate"],format = "%m/%d/%Y"))
			worksheet.write(row,0,date,get_format(workbook,*[])) 
			worksheet.write(row,1,record["client"]["fullname"],get_format(workbook,*[])) 
			worksheet.write(row,2,record["client"]["address"],get_format(workbook,*[])) 
			worksheet.write(row,3,record["client"]["gender"],get_format(workbook,*[])) 
			worksheet.write(row,4,record["client"]["ethnicity_race"],get_format(workbook,*[])) 
			worksheet.write(row,5,record["client"]["ethnicity_hispanic_origin"],get_format(workbook,*[])) 
			worksheet.write(row,6,record["client"]["occupation"],get_format(workbook,*[])) 
			worksheet.write(row,7,birthdate,get_format(workbook,*[])) 
			worksheet.write(row,8,record["available_capacity"],get_format(workbook,*[])) 
			worksheet.write(row,9,record["capacity"],get_format(workbook,*[]))

			top_sites = record.get("top_sites",[])

			current_row = row
			for top_site in top_sites:
				current_row += 1

				worksheet.write(current_row,10,top_site["title"],get_format(workbook,*[]))
				worksheet.write(current_row,11,top_site["url"],get_format(workbook,*[]))

			row = current_row


		workbook.close() 
		output.seek(0) 
		response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet") 
		title="browser_info"
		response['Content-Disposition'] = "attachment; filename="+title+".xlsx"
		
		return response
	except Exception as e:
		print(e)
		return error(e)
