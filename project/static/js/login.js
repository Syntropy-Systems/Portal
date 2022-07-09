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
		me.registration_data = {};
		me.registration_data["email"] = "testemail@gmail.com"
		me.registration_data["firstname"] = "Test First Name"
		me.registration_data["lastname"] = "Test Last Name"
		me.registration_data["address"] = "Test Address"
		me.registration_data["gender"] = "male"
		me.registration_data["birthdate"] = new Date(moment());
		me.registration_data["ethnicity_race"] = "asian"
		me.registration_data["ethnicity_hispanic_origin"] = "false"
		me.registration_data["occupation"] = "in_person"
		me.registration_data["password"] = "123123"
		me.registration_data["repassword"] = "123123"


		me.open_dialog("/register/create_dialog/","dialog_height_60 dialog_width_30");
	}

	me.register = function(){
		registration_data = angular.copy(me.registration_data);
		registration_data = me.format_date(registration_data);

		var post = me.post_generic("/register/",registration_data,"dialog")
		post.success(function(response){
			Notification.success("Thank you for choosing WeProBPO!.","Successfully registered.",10000000);
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