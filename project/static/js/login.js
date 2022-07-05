var app = angular.module("login_page",['common_module']);

app.controller('loginCtrl', function($scope,$http,$controller,CommonFunc,CommonRead,Notification){
	angular.extend(this, $controller('CommonCtrl', {$scope: $scope}));
	var me = this;

	me.login_data = {};
	me.registration_data = {"is_bpo": true,"is_va": false};
	me.login = function(){
		var post = me.post_generic("/login/submit/",me.login_data,"main",true)
		post.success(function(response){
			setTimeout(function () { window.location = "/"; }, 1500);
		})
	}

	me.registration_dialog = function(){
		me.registration_data = {"is_bpo": true,"is_va": false};
		me.open_dialog("/register/create_dialog/","dialog_height_60 dialog_width_30");
	}

	me.register = function(){
		var post = me.post_generic("/register/",me.registration_data,"dialog")
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