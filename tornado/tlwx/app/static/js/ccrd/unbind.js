$(function(){
    $('#submit').on('click', function(){
        $.post(BASE_URL + '/ccrd/unbind', function(resp){
            if(resp.success){
                window.location.href = BASE_URL + '/staticfile/done.html?from=unbind';
            }else{
                $.toptips(resp.msg);
            }
        });
    });
});
