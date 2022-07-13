var app = angular.module("login_page",['common_module']);

app.controller('loginCtrl', function($scope,$http,$controller,CommonFunc,CommonRead,Notification){
	angular.extend(this, $controller('CommonCtrl', {$scope: $scope}));
	var me = this;

	me.login_data = {};
	me.registration_data = {}

	me.login = function(){
		var post = me.post_generic("/login/submit/",me.login_data,"main",true)
		post.success(function(response){
			setTimeout(function () { window.location = "/"; }, 1500);
		})
	}

	me.registration_dialog = function(){
		rand_num = Math.floor(Math.random() * 10000)

		me.registration_data = {};
		me.registration_data["email"] = "testemail"+rand_num+"@gmail.com"
		me.registration_data["firstname"] = "Alde"
		me.registration_data["lastname"] = "Sabido"
		me.registration_data["address"] = "Address"
		me.registration_data["country"] = "State"
		me.registration_data["city"] = "City"
		me.registration_data["zip_code"] = "98899"
		me.registration_data["gender"] = "male"
		me.registration_data["birthdate"] = new Date(moment());
		me.registration_data["ethnicity_race"] = "asian"
		me.registration_data["ethnicity_hispanic_origin"] = "false"
		me.registration_data["occupation"] = "in_person"
		me.registration_data["password"] = "123123"
		me.registration_data["repassword"] = "123123"


		me.open_dialog("/register/create_dialog/","dialog_height_60 dialog_width_40");
	}

	me.register = function(){
		registration_data = angular.copy(me.registration_data);
		registration_data = me.format_date(registration_data);

		var post = me.post_generic("/register/",registration_data,"dialog")
		post.success(function(response){
			Notification.success("Thank you for choosing Syntropy!","Successfully registered.",10000000);
			me.close_dialog();
		})

		post.error(function(response){
			Notification.error(response);
		})
	}

	me.on_load = function(){
		var current_url = window.location.href;
		if(current_url.indexOf("#") >= 0){
	        var splitted_url = current_url.split("#");
	        if(splitted_url[1] == "register"){
	        	me.registration_dialog();
	        }
	    }
	}

	me.on_load();
});