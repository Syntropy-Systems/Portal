

def extract_token(request):
	request_meta = request.META
	token = None

	if request_meta:
		authorization_header = request_meta.get("HTTP_AUTHORIZATION","")
		if "token" in authorization_header.lower():
			authorization_header_splitted = authorization_header.split(" ")
			token = authorization_header_splitted[-1]
	return token
