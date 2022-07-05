var app = angular.module("users",['common_module','ui.router']);

app.controller('usersCtrl', function($scope,$http,$controller,$state,CommonFunc,CommonRead,CommonFac){
    angular.extend(this, $controller('CommonCtrl', {$scope: $scope}));
    var me = this;

    var btnstandby = "btn btn-default btn-w-m";
    var btnactive = "btn btn-success btn-w-m";
    me.current_tab = "Client";
    me.reset_tab_status = function(){
        me.btnclass = {
            "Client": btnstandby,
            "CDA": btnstandby,
            "Admin": btnstandby,
        }
    }

    me.change_tab = function(tab){
        me.reset_tab_status();
        me.btnclass[tab] = btnactive;
        me.current_tab = tab;
        me.read_pagination(true);
    }

    me.create_dialog = function(record){
        me.reset_data();
        console.log(me.record)
        if(record){
            me.record = angular.copy(record);
        }
        me.record["user_type"] = me.current_tab.toLowerCase();
        me.open_dialog("/users/create_dialog/","");
    }

    me.create = function(){
        var post = me.post_generic("/register/",me.record,"main",true,false,true)
        post.success(function(response){
            me.read_pagination();
        })
    }

    me.read_pagination = function(reset){
        if(reset){me.filters = {};}
        me.filters["sort"] = me.sort;
        me.filters["user_type"] = me.current_tab;
        var filters = angular.copy(me.filters);
        filters["pagination"] = me.pagination;
        var post = me.post_generic("/users/read_pagination/",filters,"main")
        post.success(function(response){
            me.records = response.data;
            me.generate_pagination(me,response);
        });
    };

    me.load_to_edit = function(record){
        var post = me.post_generic("/users/load_to_edit/"+record.id,{},"main")
        post.success(function(response){
            me.create_dialog(response);
        })
    }

    me.delete = function(record,delete_forever){
        if(record.is_active){
            var message = "Inactive "+record.fullname+"?";
        }else{
            var message = "Active "+record.fullname+"?";
        }

        var confirmation = CommonFunc.confirmation(message);
        confirmation.then(function(){
            var post = me.post_generic("/users/delete/"+record.id+"/",{"delete_forever":delete_forever},"main",true)
            post.success(function(response){
                me.read_pagination();
            })
        })
    }


    me.change_password_dialog = function(record){
        me.current_record = record;
        me.record = {"id": record.id};
        me.open_dialog("/users/change_password_dialog/","");
    }

    me.change_password = function(record){
        var post = me.post_generic("/users/change_password/",me.record,"main",true,false,true)
    }


    me.reset_data = function(){
        me.record = {};
    }


    me.main_loader = function(reset){
        me.read_pagination(reset);    
    }

    me.change_tab('Client');
});
