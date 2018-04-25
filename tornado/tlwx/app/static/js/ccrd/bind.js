$(function(){
    next = getUrlArgs('next');
    console.log(next);
    $('form').form();

    $('.ys_agree_clause').on('click', function(){
        $('.ys_fixed_footer').addClass('clause_btn_visible');
    });
    $('.ys_fixed_footer').on('click', function(){
        $(this).removeClass('clause_btn_visible');
    });

    $('#get_vcode').on('click', function(){
        $(this).infoCheck();
    });

    $('#submit').on('click', function(){
        validate_res = false;
        $('form').validate(function(error){
            if(!error) validate_res = true;
        });
        if (!validate_res) return false;

        var encrypt = new JSEncrypt();
        encrypt.setPublicKey(PUB_KEY);
        data = JSON.stringify({
            'ccrdno': $('input[name="ccrdno"]').val(),
            'vcode': $('input[name="vcode"]').val(),
        });
        data = encrypt.encrypt(data);
        $.post(BASE_URL + '/ccrd/bind', data, function(resp){
            if(resp.success){
                window.location.href = BASE_URL + '/staticfile/done.html?from=bind';
            }else{
                $.toptips(resp.msg);
            }
        });
    });
});
