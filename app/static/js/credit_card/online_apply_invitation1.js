$(function(){
    $('#form1').form();
    $('#submit1').on('click', function(){
        validate_res = false;
        $('#form1').validate(function(error){
            if(!error) validate_res = true;
        });
        if (!validate_res) return false;
        data = JSON.parse($('#form1').serializeForm());
        window.location.href = 'online_apply_invitation2.html?name=' +
            data.name + '&employee_id=' + data.employee_id;
    });
})
