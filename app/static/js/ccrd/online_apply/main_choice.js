$(function(){

    $('#submit').on('click', function(){
        product_cd = ['A001', 'A002', 'B01', 'B02'][rd(0, 3)]
        data = JSON.stringify({
            'product_cd': product_cd,
        });
        $.post('', data, function(resp){
            console.log(resp);
            if(resp.success){
                setCookie('product_cd', product_cd);
                window.location.href = './base_info';
            }else{
                $.toptips(resp.msg);
            }
        });
    });

});
