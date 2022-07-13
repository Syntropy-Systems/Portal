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
		records = Order.objects.filter(**filters).order_by(*sort_by)

		if not user_instance.is_developer:
			records = records.filter(client = user_instance.pk)

		if not from_export:
			results.update(generate_pagination(pagination,records))
			records = records[results['starting']:results['ending']]

		for record in records:
			row = record.as_dict()
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
		worksheet.write(row,2,"Available Capacity",get_format(workbook,*["bold"])) 
		worksheet.set_column(2,2,15) 
		worksheet.write(row,3,"Capacity",get_format(workbook,*["bold"])) 
		worksheet.set_column(3,3,15) 
		worksheet.write(row,4,"Site Name",get_format(workbook,*["bold"])) 
		worksheet.set_column(4,4,30) 
		worksheet.write(row,5,"Site URL",get_format(workbook,*["bold"])) 
		worksheet.set_column(5,5,30) 


		for record in records:
			row += 1 

			date = str(date_to_str(record["date"],format = "%m/%d/%Y"))
			worksheet.write(row,0,date,get_format(workbook,*[])) 
			worksheet.write(row,1,record["client"]["fullname"],get_format(workbook,*[])) 
			worksheet.write(row,2,record["available_capacity"],get_format(workbook,*[])) 
			worksheet.write(row,3,record["capacity"],get_format(workbook,*[]))

			top_sites = record.get("top_sites",[])

			current_row = row
			print(current_row)
			for top_site in top_sites:
				current_row += 1

				worksheet.write(current_row,4,top_site["title"],get_format(workbook,*[]))
				worksheet.write(current_row,5,top_site["url"],get_format(workbook,*[]))

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
