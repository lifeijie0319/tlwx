$(function(){
    $('select[name="id_type"]').val('I');
    $('#form1').form();

    $('#send_vcode').on('click', function(){
         $(this).sendVcode($('input[name="cellphone"]'));
    });

    $('#submit1').on('click', function(){
        validate_res = false;
        $('#form1').validate(function(error){
            if(!error) validate_res = true;
        });
        if (!validate_res) return false;

        data = $('#form1').serializeForm();
        $.post('./base_info', data, function(resp){
            console.log(resp);
            if(resp.success){
                window.location.href = './id_card';
            }else{
                $.toptips(resp.msg);
            }
        });
    });

});
