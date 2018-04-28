$(function(){
    $.get(BASE_URL + '/static/doc/ccrd/3.txt', function(resp){
        $('#protocol3').html('<pre>' + resp + '</pre>');
    }); 
    $('.ys_agree_clause').on('click', function(){
        $('.ys_fixed_footer').addClass('clause_btn_visible');
    });
    $('.ys_fixed_footer').on('click', function(){
        $(this).removeClass('clause_btn_visible');
    });

    $('#form6').form();

    $('#submit6').on('click', function(){
        validate_res = false;
        $('#form6').validate(function(error){
            if(!error) validate_res = true;
        });
        if (!validate_res) return false;

        data = $('#form6').serializeForm();
        $.post('', data, function(resp){
            console.log(resp);
            if(resp.success){
                window.location.href = './face_check';
            }else{
                $.toptips(resp.msg);
            }
        });
    });
});
