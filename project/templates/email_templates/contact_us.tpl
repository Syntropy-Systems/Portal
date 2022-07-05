{% extends "mail_templated/base.tpl" %}
{% block subject %}
	Contact Us Message
{% endblock %}

{% block html %}
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    </style>
</head>

<body yahoo bgcolor="#ffffff">
</body>
	<h3><center>{{firstname}}</center></h3>
	<b>Message</b> : {{message}}<br>
	<b>Email</b> : {{email}}<br>
</html>

{% endblock %}
 