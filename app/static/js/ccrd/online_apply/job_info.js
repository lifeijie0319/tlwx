$(function(){
    $('#form4').form();

    $('#submit4').on('click', function(){
        validate_res = false;
        $('#form4').validate(function(error){
            if(!error) validate_res = true;
        });
        if (!validate_res) return false;
        window.location.href = '5';
    });
});
