$(function(){
    txn_date = getUrlArgs('txn_date').replace('-', '');
    txn_amt = getUrlArgs('txn_amt');
    ref_nbr = getUrlArgs('ref_nbr');

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
    });
    $('form').form();
    $('select[name="num"]').on('change', function(){
        option = $(this).find('option:selected');
        $('input[name="min_amount"]').val(option.attr('min_amount'));
        $('input[name="max_amount"]').val(option.attr('max_amount'));
        data = JSON.stringify({
            'CURR_CD': '156',
            'TXN_DATE': txn_date,
            'TXN_AMT': txn_amt,
            'REF_NBR': ref_nbr,
            'LOAN_INIT_TERM': $('select[name="num"]').val(),
            'LOAN_FEE_METHOD': $('select[name="fee_method"]').val(),
            'OPT': '0',
        });
        $.post(BASE_URL + '/ccrd/installment/bill', data, function(resp){
            console.log(resp);
            if(resp.success){
                $('input[name="period_pay"]').val(resp.loan_fixed_pmt_prin);
                $('input[name="total_fee"]').val(resp.loan_init_fee1);
                $('input[name="stage_fee"]').val(resp.loan_fixed_fee1);
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
        if (!validate_res){
            $(this).val('');
            return false;
        }
        data = JSON.stringify({
            'CURR_CD': '156',
            'TXN_DATE': txn_date,
            'TXN_AMT': txn_amt,
            'REF_NBR': ref_nbr,
            'LOAN_INIT_TERM': $('select[name="num"]').val(),
            'LOAN_FEE_METHOD': $('select[name="fee_method"]').val(),
            'OPT': '1',
        });
        $.post(BASE_URL + '/ccrd/installment/bill', data, function(resp){
            console.log(resp);
            if(resp.success){
                window.location.href = BASE_URL + '/staticfile/done.html?from=installment_consumption';
            }else{
                $.toptips(resp.msg);
            }
        });
    });
});
