$(function(){
    from = getUrlArgs('from');
    switch(from){
        case 'bind':
            $('#content').html('绑定信用卡成功');
            break;
        case 'unbind':
            $('#content').html('解绑信用卡成功');
            break;
        case 'ccrd_online_apply':
            $('#content').html('您的信用卡申请已提交，请等待银行审核');
            break;
        default:
    }
});
