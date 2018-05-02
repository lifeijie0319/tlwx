$(function(){
    $('.ys_agree_clause').on('click', function(){
        $('.ys_fixed_footer').addClass('clause_btn_visible');
    });     
    $('.ys_fixed_footer').on('click', function(){
        $(this).removeClass('clause_btn_visible');
    });

    $('input[name="agree"]').on('change', function(){
        //console.log($(this).prop('checked'));
        if($(this).prop('checked')){
            $('#submit').prop('disabled', false);
        }else{
            $('#submit').prop('disabled', true);
        }
    }).trigger('change');

    $('form').form();
    $('select[name="num"]').on('change', function(){
        max_stage_amt = $(this).find('option:selected').attr('loan_amt');
        $('input[name="max_stage_amt"]').val(max_stage_amt);
        total_amt = $('input[name="total_amt"]');
        validate_res = false;
        total_amt.parents('.ys_cell').validate(function(error){
            if(!error) validate_res = true;
        });
        if (!validate_res){
            $(this).val('');
            return false;
        }
        total_amt_val = parseInt(total_amt.val());
        max_stage_amt = parseInt(max_stage_amt);
        if(total_amt_val > max_stage_amt){
            $.toptips('分期金额不能大于最高可分期金额');
            $(this).val('');
            return false;
        }
        data = JSON.stringify({
            'CURR_CD': '156',
            'LOAN_INIT_TERM': $('select[name="num"]').val(),
            'CASH_AMT': total_amt.val(),
            'LOAN_FEE_METHOD': $('select[name="fee_method"]').val(),
            'OPT': '0',
        });
        $.post(BASE_URL + '/ccrd/installment/cash', data, function(resp){
            console.log(resp);
            if(resp.success){
                $('input[name="staging_pay"]').val(resp.loan_fixed_pmt_prin);
                $('input[name="total_fee"]').val(resp.loan_init_fee1);
                $('input[name="stage_fee"]').val(resp.loan_fixed_fee1);
            }else{
                $.toptips(resp.msg);
                $('select[name="num"]').val('');
            }
        });
    });
    $('#submit').on('click', function(){
        validate_res = false;
        $('form').validate(function(error){
            if(!error) validate_res = true;
        });
        if (!validate_res){
            $(this).val('');
            return false;
        }
        data = JSON.stringify({
            'CURR_CD': '156',
            'LOAN_INIT_TERM': $('select[name="num"]').val(),
            'CASH_AMT':  $('input[name="total_amt"]').val(),
            'LOAN_FEE_METHOD': $('select[name="fee_method"]').val(),
            'OPT': '1',
        });
        $.post(BASE_URL + '/ccrd/installment/cash', data, function(resp){
            console.log(resp);
            if(resp.success){
                window.location.href = BASE_URL + '/staticfile/done.html?from=installment_cash';
            }else{
                $.toptips(resp.msg);
            }
        });
    });
});
