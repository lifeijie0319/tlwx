$(function(){

    $('#submit').on('click', function(){
        data = JSON.stringify({
            'product_cd': 'A0023',
        });
        $.post('./choice', data, function(resp){
            console.log(resp);
            if(resp.success){
                window.location.href = './base_info';
            }else{
                $.toptips(resp.msg);
            }
        });
    });

});
