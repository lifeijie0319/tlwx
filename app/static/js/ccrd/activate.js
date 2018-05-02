$(function(){

    $("form").form();
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

        data = JSON.stringify({
            'ccrdno': $('input[name="ccrdno"]').val(),
            'expire': $('input[name="expire"]').val(),
            'cvv2': $('input[name="cvv2"]').val(),
            'vcode': $('input[name="vcode"]').val()
        });
        console.log(data, data.length, PUB_KEY.length);
        var encrypt = new JSEncrypt();
        encrypt.setPublicKey(PUB_KEY);
        data = encrypt.encrypt(data);

        $.post('', data, function(resp){
            if(resp.success){
                window.location.href = BASE_URL + '/staticfile/done.html?from=activate';
            }else{
                $.toptips(resp.msg);
            }
        });
    });
});
