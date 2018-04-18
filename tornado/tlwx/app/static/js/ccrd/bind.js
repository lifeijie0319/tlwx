$(function(){
    $('form').form();

    $('#get_vcode').on('click', function(){
        validateRes = false;
        $('form').validate(function (error) {
            if (error) {
                dom_name = error.$dom.attr('name');
                console.log(dom_name);
                if(dom_name == 'vcode'){
                    validateRes = true;
                    return true;
                }
                return false;
            } else {
                validateRes = true;
            }
        });
        if (!validateRes) return;

        data = JSON.stringify({
            action: 'info_check',
            idno: $('input[name="idno"]').val(),
            ccrdno: $('input[name="ccrdno"]').val(),
        });
        $.post(BASE_URL + '/ccrd/bind', data, function(resp){
            console.log(resp);
            if(resp.success){
                tips = '即将向尾号为' + resp.cellphone.slice(-4) + '的手机发送短信验证码，请确认';
                title = '短信验证码发送确认';
                $.confirm(tips, title, function(){
                    $('#get_vcode').sendVcode($('input[name="cellphone"]'));
                },function(){
                    console.log('cancel');
                });
            }else{
                $.toptips(resp.msg);
            }
        });
    });

    $('#submit').on('click', function(){
        validate_res = false;
        $('form').validate(function(error){
            if(!error) validate_res = true;
        });
        if (!validate_res) return false;

        data = $('form').serializeForm();
        $.post(BASE_URL + '/ccrd/bind', data, function(resp){
            if(resp.success){
                window.location.href = BASE_URL + '/staticfile/done.html?from=bind';
            }else{
                $.toptips(resp.msg);
            }
        });
    });
});
