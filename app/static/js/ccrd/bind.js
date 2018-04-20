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

        data = $('form').serializeForm();
        data = JSON.parse(data);
        data['action'] = 'submit';
        delete data.agree;
        console.log(data);
        data = JSON.stringify(data);
        $.post(BASE_URL + '/ccrd/bind', data, function(resp){
            if(resp.success){
                window.location.href = BASE_URL + '/staticfile/done.html?from=bind';
            }else{
                $.toptips(resp.msg);
            }
        });
    });
});
