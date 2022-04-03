function POST_API(data,endpoint){
    $.ajax({ type: "POST",   
                         url: endpoint,  
                         dataType: "json",
                         contentType: 'application/json',
                         data:JSON.stringify( data ),
                         success : function(resp)
                         {
                             return resp
                         }
                });
}

function GET_API(data,endpoint){
    $.ajax({ type: "POST",   
                         url: endpoint,  
                         dataType: "json",
                         contentType: 'application/json',
                         data:JSON.stringify( data ),
                         success : function(resp)
                         {
                             return resp
                         }
                });
}

function GET_API(endpoint){
    $.ajax({ type: "POST",   
                         url: endpoint,  
                         dataType: "json",
                         contentType: 'application/json',
                         success : function(resp)
                         {
                             return resp
                         }
                });
}