$(function(){
    $('#form5').form();

    $('#submit5').on('click', function(){
        validate_res = false;
        $('#form5').validate(function(error){
            if(!error) validate_res = true;
        });
        if (!validate_res) return false;
        window.location.href = '6';
    });
});
