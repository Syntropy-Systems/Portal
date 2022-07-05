var app = angular.module("dashboard",['common_module','ui.router','ui.calendar']);

app.controller('dashboardCtrl', function($scope,$http,$controller,$state,CommonFunc,CommonRead,CommonFac){
    angular.extend(this, $controller('CommonCtrl', {$scope: $scope}));
    var me = this;

    me.record = {};
    me.create_schedule_dialog = function(){
        me.open_dialog("/dashboard/create_schedule_dialog/");
    }

    me.create_schedule = function(){
        var post = me.post_generic("/dashboard/create_schedule/",me.record,"dialog",true,false,true)
        post.success(function(response){
            me.read_schedules();
        })
    }

    me.setup_calendar = function(){
        
    }


    me.read_schedules = function(){
        $scope.uiConfig = {
            calendar:{
                // height: 450,
                eventLimit: true,
                views: {
                    agenda: {
                        eventLimit: 1 // adjust to 6 only for agendaWeek/agendaDay
                    }
                },
                editable: false,
                selectable : false,
                navLinks: true,
                customButtons: {
                    myCustomButton: {
                        text: 'add event',
                        click: function() {
                            $scope.create_announcement_dialog()
                        }
                    },
                    filterButton: {
                        text: 'filter',
                        click: function() {
                            $scope.calendar_filter_dialog()
                        }
                    }
                },
                header: {
                    left: 'prev,next today',
                    center: 'title',
                    right: 'myCustomButton filterButton month,agendaWeek,agendaDay,listWeek'
                },
                viewRender: function(view, element) {
                    var moment = $('#calendar').fullCalendar('getDate');
                    // $scope.read_announcement_pagination(moment)
                },
                eventRender: function (event, element) {
                    element.attr('href', 'javascript:void(0);');
                    element.click(function() {
                        if(event.end == null){
                            event.end = event.start
                        }
                        $scope.create_announcement_dialog(event)
                    });
                }
            }
        };


        $scope.events = [];
        me.eventSources = [{events: $scope.events, textColor:'white' }];
        var post = me.post_generic("/dashboard/read_schedules/",{},"main")
        post.success(function(records){
            for(var i in records){
                row = {"title": records[i].title}
                row.start = new Date(records[i].date_from);
                row.end = new Date(records[i].date_to);
                $scope.events.push(row)
            }
        })
    }

    me.read_schedules();






    


    // var date = new Date();
    // var d = date.getDate();
    // var m = date.getMonth();
    // var y = date.getFullYear();
    // console.log(new Date(y, m, 1))

    // $scope.events = [
    //       {title: 'GY - Jen',start: new Date(y, m, 1)},
    //       {title: 'GY - Matt',start: new Date(y, m, 2)},
    //       {title: 'GY - Parlem',start: new Date(y, m, 3)},
    //       {title: 'GY - Nona',start: new Date(y, m, 4)},
    //       {title: 'Bill Morgan',start: new Date(y, m, 4)},
    //       {title: 'Bill Natasha',start: new Date(y, m, 4)},
    //       {title: 'GY - Cindy Baby',start: new Date(y, m, 5)},
    //       {title: 'Bill Deon',start: new Date(y, m, 5)},
    //       {title: 'Bill Stacey',start: new Date(y, m, 15)},
    // ];
    // // console.log($scope.events)
    // me.eventSources = [{events: $scope.events, textColor:'white' }];

    // return;

    
});
