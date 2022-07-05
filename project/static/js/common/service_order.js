var app = angular.module('service_order', [])
app.factory("QC", function(CommonFunc){
    return {
        open_dialog: function(scope,record,not_open_dialog){
            loader = "main";
            if(not_open_dialog){
                loader = "dialog";
            }

            scope.qc_record = {};
            scope.current_record = record;
            var post = scope.post_generic("/orders/read_qcs/"+record.id,{},loader)
            post.success(function(response){
                scope.notes = scope.list_format_date(response,false,true);
                if(!not_open_dialog){
                    scope.open_dialog("/orders/qc_dialog/","notes_dialog");
                }
            })
        },
        create: function(scope,qc,custom_record){
            if(!qc){
                return;
            }

            var record = scope.current_record;
            if(custom_record){
                record = custom_record;
            }

            var me = this;
            var post = scope.post_generic("/orders/create_qc/"+record.id,{"note": qc},"dialog")
            post.success(function(response){
                me.open_dialog(scope,record,true);
            })
        },
        delete: function(scope,qc){
            var me = this;
            var confirmation = CommonFunc.confirmation();
            confirmation.then(function(){
                var post = scope.post_generic("/orders/delete_qc/"+scope.current_record.id+"/"+qc.id,{},"dialog",true)
                post.success(function(response){
                    me.open_dialog(scope,scope.current_record,true);
                })
            })
        }
    }
})

app.factory("Notes", function(CommonFunc){
    return {
        open_dialog: function(scope,record,not_open_dialog){
            loader = "main";
            if(not_open_dialog){
                loader = "dialog";
            }

            scope.notes_record = {}
            scope.current_record = record;
            var post = scope.post_generic("/orders/read_notes/"+record.id,{},loader)
            post.success(function(response){
                scope.notes = scope.list_format_date(response,false,true);
                if(!not_open_dialog){
                    scope.open_dialog("/orders/notes_dialog/","notes_dialog");
                }
            })
        },
        create: function(scope,note,custom_record){
            if(!note){
                return;
            }
            var me = this;

            var record = scope.current_record;
            if(custom_record){
                console.log("yeah!")
                record = custom_record;
            }

            var post = scope.post_generic("/orders/create_note/"+record.id,{"note": note},"dialog")
            post.success(function(response){
                me.open_dialog(scope,record,true);
            })
        },
        delete: function(scope,note){
            var me = this;
            var confirmation = CommonFunc.confirmation();
            confirmation.then(function(){
                var post = scope.post_generic("/orders/delete_note/"+scope.current_record.id+"/"+note.id,{},"dialog",true)
                post.success(function(response){
                    me.open_dialog(scope,scope.current_record,true);
                })
            })
        }
    }
})

app.factory("Photos", function(CommonFunc){
    return {
        open_dialog: function(scope,record) {
            scope.file_added = false;
            scope.current_record = record;
            var me = this;

            var post = this.read(scope);
            post.success(function(response){
                scope.open_dialog("/orders/photos_dialog/","width80");
            })
        },
        read: function(scope){
            var post = scope.post_generic("/orders/photos_read/"+scope.current_record.id+"/",{},"main")
            return post.success(function(response){
                scope.photos = response;
            })
        },
        remove: function(scope,photo){
            var me = this;
            var confirmation = CommonFunc.confirmation("Remove?",false,false,"Continue");
            confirmation.then(function(){
                var post = scope.post_generic("/orders/photos_remove/"+scope.current_record.id+"/"+photo.id+"/",{},"dialog",true);
                post.success(function(){
                    me.read(scope);
                })
            })
        }
    }
})

app.factory("Documents", function(CommonFunc){
    return {
        open_dialog: function(scope,record) {
            scope.file_added = false;
            scope.current_record = record;
            var me = this;

            var post = this.read(scope);
            post.success(function(response){
                scope.open_dialog("/orders/docs_dialog/","width80");
            })
        },
        read: function(scope){
            var post = scope.post_generic("/orders/docs_read/"+scope.current_record.id+"/",{},"main")
            return post.success(function(response){
                scope.documents = response;
            })
        },
        remove: function(scope,doc){
            var me = this;
            var confirmation = CommonFunc.confirmation("Remove?",false,false,"Continue");
            confirmation.then(function(){
                var post = scope.post_generic("/orders/docs_remove/"+scope.current_record.id+"/"+doc.id+"/",{},"dialog",true);
                post.success(function(){
                    me.read(scope);
                })
            })
        }
    }
})