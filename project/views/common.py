from django.shortcuts import render, get_object_or_404,redirect
from django.utils.dateparse import parse_date
from django.db import models
from django.db.models import Count, Sum, Avg,Min,Q,F,Func
from math import ceil,floor
from django.http import HttpResponse,JsonResponse,StreamingHttpResponse
from random import randint
from datetime import datetime,timedelta,date
from copy import copy
import math,json,time,datetime as idatetime,copy as icopy,decimal,ast,csv,os,copy,re
from django.core import serializers
from operator import itemgetter
from decimal import Decimal
from time import mktime
from django.utils.termcolors import colorize
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.encoding import smart_str
from django.conf import settings
from collections import OrderedDict
from django.db.models.functions import Coalesce
from django.forms.models import model_to_dict
from django.utils import timezone
from mail_templated import send_mail
from django.apps import apps
from django.views.decorators.http import require_GET, require_POST
import io
import xlsxwriter


'''
	Just like a Decimal() function but changes the None into 0
'''
class DDecimal(Decimal) :
    def __new__ (self,value=0):
    	if value == None or value == False:
    		value = 0
    	return Decimal(value)

    	
def round_decimal(value, places = 2):
	if not value:
		value = 0

	value = DDecimal(value)
	rounded_off = value.quantize(Decimal(10) ** -places)
	return rounded_off


'''
	Decimal and Date Encoder
'''
class DecimalDateEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, Decimal):
			return float("%.14f" % obj)

		if isinstance(obj, idatetime.date):
			if isinstance(obj, datetime):
				return str(obj)
			else:
				return str(obj)

		return json.JSONEncoder.default(self, obj)

def post_data(request):
	post_params = json.loads(request.body.decode("utf-8")) if request.body.decode("utf-8") else {}
	return post_params

'''
	colored print in terminal
	str_to_print = The string that you want to print
	fg = color of the text (optional) (default to red)
	bg = background color of the text (optional) (default to white)
'''
def cprint(str_to_print, fg = "white", bg = "blue"):
	print(colorize(str_to_print, fg=fg, bg=bg))

def eprint(string, fg="white", bg="blue"):
	print ("======================================")
	print (colorize(string, fg=fg, bg=bg))
	print ("======================================")

def dprint(string):
	print ("======================================")
	print (string)
	print ("======================================")

'''
	Gets the current date and return depends on what format you want to return
'''

def current_date(to_return = None):
	if to_return == 'month':
		return datetime.today().month
	elif to_return == 'year':
		return datetime.today().year
	elif to_return == 'day':
		return datetime.today().day
	else:
		return datetime.today().date()


	
def values_list(listt,column = "id",allow_duplicates = True,allow_none = True):
	v_list = []
	for obj in listt:
		if isinstance(obj,int):
			col_value = obj
		else:
			col_value = obj.get(column,None)
			
		if not allow_duplicates:
			if col_value in v_list:
				continue

		if col_value == None and not allow_none:
			continue
		
		v_list.append(col_value)
	return v_list;

'''
	Remove duplicates for lists
'''
def remove_duplicates(var_list,remove_none = False):
	new_list = []
	for i in var_list:
		if remove_none and i == None:
			continue

		if i not in new_list:
			new_list.append(i)
	return new_list

'''
	just call this function for testing stopper
	instead of calling raise ValueError('test'), just use raise_error() function
'''

def raise_error(msg = "Testing Stopper",is_json_dump = False):
	if is_json_dump:
		msg = json.dumps(msg)
	raise ValueError(msg)

def success_list(to_return_list, to_list = True):
	if to_list:
		to_return_list = to_return_list if to_return_list else []
		to_return_list = list_dates_to_str(to_return_list)
	else:
		to_return_list = to_return_list if to_return_list else {}
		to_return_list = obj_dates_to_str(to_return_list)
	to_return_list = json_encode(to_return_list,to_list)
	return HttpResponse(to_return_list, status = 200)

def success_obj(listt):
	listt = listt if listt else {}
	return HttpResponse(json_encode(listt), status = 200)

def success(to_return = "Successfully saved."):
	return HttpResponse(to_return, status = 200)

def error_list(listt):
	listt = listt if listt else []
	return HttpResponse(json_encode(listt), status = 400)

def error_obj(listt):
	listt = listt if listt else {}
	return HttpResponse(json_encode(listt), status = 400)

def error(to_return = "Something went wrong. Please contact your admin."):
	try:
			
		'''
			If the error is an array of an object, just show the first array index of the first object.
		'''
		has_dict = False
		first_error = None
		for str_return in to_return:
			try:
				dict_return = ast.literal_eval(str_return)
				has_dict = True
				firstkey = str_beautify(dict_return.iterkeys().next())
				firstkeyvalue = str_beautify(dict_return.itervalues().next()[0])
				first_error = firstkeyvalue
				if firstkey not in ["all","All","  all  "]:
					first_error = firstkey+" : "+firstkeyvalue
				else:
					exploded = 	first_error.split('with this client and ')
					if len(exploded) > 1:
						first_error = str_beautify(exploded[1])
				continue
			except Exception as e:
				has_dict = False

		if has_dict:
			to_return = first_error
		else:
			to_return = str_beautify(to_return)
			print(to_return)

		return HttpResponse(to_return, status = 400)
	except Exception as e:
		print(e)
		return HttpResponse(to_return, status = 400)


#If the key value is obj, set the id.
def clean_obj(data,array_field = False):
	try:
		for key in data:
			if isinstance(data[key], dict):
				if 'id' in data[key]:
					data[key] = data[key]['id']

		if array_field:
			for key in data:
				if isinstance(data[key], list):
					data[key] = list2str(values_list(data[key]))

		return data
	except Exception as e:
		print(e)

def list2str(arr,separator=","):
	return separator.join(map(str, arr))


def str_beautify(str_to_convert,delimeter = "_"):
	str_to_convert = str(str_to_convert)
	to_return = str_to_convert.replace ("__", "")
	to_return = to_return.replace ("_", " ")
	return to_return.capitalize()


'''
	instead of using json.dumps(list(list_value)) you can use json_encode()
'''

def json_encode(var_list,use_list_function = True):
	if use_list_function:
		var_list = list(var_list)

	return json.dumps(var_list, cls = DecimalDateEncoder)


'''
	lists = a list that contains date(s) that needs to be converted into string
	remove_time = Defaults to True; if false, leave the date as is.
	TODO: needs to remove date_resolved and replace it to dynamic type date
'''

def list_dates_to_str(lists):
	results = []
	for value in lists:
		if isinstance(value,dict):
			results.append(obj_dates_to_str(value))
		else:
			results.append(value)

	return results

def obj_dates_to_str(objs,remove_time = False):
	try:
		for key,value in objs.items():
			if isinstance(objs[key], idatetime.date):

				if isinstance(objs[key], datetime) and remove_time:
					objs[key] = str(objs[key].date())
				else:
					objs[key] = str(objs[key].strftime("%Y-%m-%d %I:%M:%p"))

		objs = obj_decimal_to_float(objs)
		return objs
	except Exception as e:
		raise ValueError(e)

def list_decimal_to_float(lists):
	results = []
	for value in lists:
		results.append(obj_decimal_to_float(value))

	return results

def obj_decimal_to_float(objs):
	try:
		for key,value in objs.items():
			if isinstance(objs[key], decimal.Decimal):
				objs[key] = float(objs[key])

		return objs
	except Exception as e:
		raise ValueError(e)

def date_to_str(date,format = "%B %d, %Y"):
	return datetime.strftime(date, format)

def str2model(model_name,get_instance = False,filters = {}):
	model = apps.get_model(app_label='project', model_name=model_name)
	if get_instance:
		model = model.objects.get(**filters)
	return model


'''
	Calculate the total_records,total_pages and the start and end of the query.
'''
def generate_sorting(sort_dict = None):
	if not sort_dict:
		sort_dict = {"sort_by" : "id","reverse" : False}

	sort_by = sort_dict.get("sort_by","id")
	if not sort_dict.get("reverse",False):
		return [sort_by,"id"]

	sort_by = "-"+sort_by
	return [sort_by,"-id"]

def generate_pagination(pagination_data,records):
	page = pagination_data["current_page"] - 1
	page_size = pagination_data["limit"]
	total_records = records.count()
	total_pages   = ceil(float(total_records) / page_size)
	starting = page * page_size 
	ending = page_size + starting
	dictt = {
		"total_records" : total_records,
		"total_pages" : total_pages,
		"starting" : starting,
		"ending" : ending,
	}
	return dictt

'''
	{"is_deleted" : True, "company" : "company_id_here"} if and
		{"and" : [{"is_deleted" : True},{"company" : "company_id_here"}]}
'''
def objs_to_and_for_q(filters = {},obj_to_transform = {},type="and"):
	if type not in filters:
		filters[type] = []
	for key in obj_to_transform.keys():
		row = {}
		row[key] = obj_to_transform[key];
		filters[type].append(row)

	return filters

def filter_obj_to_q(obj,or_q = ()):
	q_filters = Q()
	for value in obj.items():
		if value[0] in or_q:
			q_filters |= Q((value[0],value[1]))
		else:
			q_filters &= Q((value[0],value[1]))

	return q_filters

def str2obj(strobj):
	return ast.literal_eval(strobj)



"""
0	None	0	 
1	Continuous	1	-----------
2	Continuous	2	-----------
3	Dash	1	- - - - - -
4	Dot	1	. . . . . .
5	Continuous	3	-----------
6	Double	3	===========
7	Continuous	0	-----------
8	Dash	2	- - - - - -
9	Dash Dot	1	- . - . - .
10	Dash Dot	2	- . - . - .
11	Dash Dot Dot	1	- . . - . .
12	Dash Dot Dot	2	- . . - . .
13	SlantDash Dot	2	/ - . / - .
"""
all_formats = {
	"bold" : {"bold" : True},
	"italic" : {"italic" : True},
	"underline" : {"underline" : 10},
	"align_center" : {"align" : "center"},
	"align_left" : {"align" : "left"},
	"align_right" : {"align" : "right"},
	"money" : {"num_format" : "#,##0.00"},
	"money_dollar" : {"num_format" : "$#,##0.00"},
	"border_1" : {"border" : 1, "bold" : True},
	"border_3" : {"border" : 3, "bold" : 5},
	"border_4" : {"border" : 4, "bold" : True},
	"border_5" : {"border" : 5},
	"border_left" : {"left" : 1, "bold" : True},
	"border_right" : {"right" : 1, "bold" : True},
	"border_bottom" : {"bottom" : 1, "bold" : True},
	"top" : {"top" : 5},
	"top_total" : {"top" : 1},
	"bottom" : {"bottom" : 5},
	"bottom_total" : {"bottom" : 5},
	"bottom_total2" : {"bottom" : 6},
	"bottom_total3" : {"bottom" : 1},
	"bottom_double_line" : {"bottom" : 6},
	"left" : {"left" : 3},
	"right" : {"right" : 3},
	"indent_1" : {"indent" : 1},
	"indent_2" : {"indent" : 2},
	"font_size_10" : {"font_size" : 10},
	"font_size_12" : {"font_size" : 12},
	"font_size_14" : {"font_size" : 14},
	"date" : {'num_format': 'mm/dd/yy'},
	"bg_color" : {'bg_color' : '#dedede'},
	"border_color" : {'border_color' : '#808080'},
	"align_vjustify" : {'align' : "vjustify"},
	"vcenter" : {'align' : "vcenter"},
	"center" : {'align' : "center"},
	"text_wrap" : {'text_wrap' : "1"},
	"color_red" : {"color" : "red"}
}

def get_format(workbook,*formats):
	final_format = {}
	for formatt in formats:
		key = list(all_formats[formatt].keys())[0]
		final_format[key] = all_formats[formatt][key]

	#default here...
	if not final_format.get("font_size",None):
		final_format["font_size"] = 10

	final_format["font_name"] = "tahoma"
	return workbook.add_format(final_format)


def date_range_filter(filters,date_field = "date",date_from = "date_from",date_to = "date_to"):
	final_date = None
	report_date_str = ""

	if not filters.get(date_from,None):
		filters.pop(date_from,None)

	if not filters.get(date_to,None):
		filters.pop(date_to,None)



	if {date_from, date_to} <= set(filters):
		date_from = filters.pop(date_from) 
		date_to = filters.pop(date_to)
		filters[date_field+'__range'] = [date_from,date_to]
	elif date_from in filters:
		date_from = filters.pop(date_from) 
		filters[date_field+'__gte'] = date_from
		
	elif date_to in filters:
		date_to = filters.pop(date_to)
		filters[date_field+'__lte'] = date_to

	return filters