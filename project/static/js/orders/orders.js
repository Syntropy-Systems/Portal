var app = angular.module("orders",['common_module','ui.router']);

app.controller('ordersCtrl', function($scope,$http,$controller,$state,CommonFunc,CommonRead,CommonFac,Notification,Notes,Photos,Documents,QC){
    angular.extend(this, $controller('CommonCtrl', {$scope: $scope}));
    var me = this;
    var btnstandby = "btn btn-default btn-w-m";
    var btnactive = "btn btn-success btn-w-m";
    me.current_tab = "active";
    me.status = {
        "active": [{"value": "completed","display": "Complete"},{"value": "hold","display": "Hold"},{"value": "cancelled","display": "Cancel"}],
    }
    
    me.reset_tab_status = function(){
        me.btnclass = {
            "active": btnstandby,
        }
    }

    me.change_tab = function(tab,first){
        me.reset_tab_status();
        me.selected_status = null;
        me.selected_records = [];
        me.btnclass[tab] = btnactive;
        me.current_tab = tab;
        me.read_pagination(false);
    }

    me.read_pagination = function(reset){
        me.filters["sort"] = me.sort;
        var filters = angular.copy(me.filters);
        filters = me.format_date(filters)
        filters["pagination"] = me.pagination;
        var post = me.post_generic("/orders/read_pagination/",filters,"main")
        post.success(function(response){
            me.records = response.data;
            me.starting = response.starting;
            me.ending = response.data.length;
            me.pagination.limit_options = angular.copy(me.pagination.limit_options_orig);
            me.pagination.limit_options.push(response.total_records)
            me.pagination["total_records"] = response.total_records;
            me.pagination["total_pages"] = response.total_pages;
            me.active_count = response.active_count;
        });
    };

    me.export = function(){
        window.open("/orders/export/","_blank")        
    }

    me.main_loader = function(){
        me.read_pagination();    
    }

    me.change_tab('active',true);
});