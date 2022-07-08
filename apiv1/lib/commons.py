import json

def extract_token(request):
	request_meta = request.META
	token = None

	if request_meta:
		authorization_header = request_meta.get("HTTP_AUTHORIZATION","")
		if "token" in authorization_header.lower():
			authorization_header_splitted = authorization_header.split(" ")
			token = authorization_header_splitted[-1]
	return token


def get_post_data(request):
	post_params = json.loads(request.body.decode("utf-8")) if request.body.decode("utf-8") else {}
	return post_params