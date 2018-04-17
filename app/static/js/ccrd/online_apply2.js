$(function(){

    configJssdk(['chooseImage','uploadImage']);

    var front_id, back_id;
    $('.id_card_wrapper').on('click', function(){
        img_dom = $(this).find('img');
        if(img_dom.attr('mediaid') || img_dom.attr('mediaid')){
            $.confirm('您最多只能上传1张图片，是否删除原来的图片重新选择？', function(){
                wxUploadImg(img_dom);
            },function(){
            });
        }else{
            wxUploadImg(img_dom);
        }
    });

    $('#ensure').on('click', function(){
        front_id = $('#front_id').attr('mediaid');
        back_id = $('#back_id').attr('mediaid');
        if(!front_id){
            $.alert('请选择身份证前面影像');
            return false;
        }
        if(!back_id){
            $.alert('请选择身份证反面影像');
            return false;
        }
        params = JSON.stringify({
            imgs: [
                {
                    mediaid: front_id,
                    dirname: 'front_id',
                },
                {
                    mediaid: back_id,
                    dirname: 'back_id',
                },
            ]
        });
        $.post(BASE_URL + '/wx/upload_img', params, function(resp){
            if(resp.success){
                $.toptips('图片存储成功', 'success');
                window.location.href = '3';
            }else{
                $.toptips('图片存储失败');
            }
        }).error(function(){
            $.toptips('服务器错误');
        });
        /*params = {
            front_id: front_id,
            back_id: back_id,
        }
        $.post(BASE_URL + '/ccrd/online_apply/upload_idcard', params, function(resp){
            if(resp.success){
                $.toptips('图片存储成功', 'success');
                window.location.href = '3';
            }else{
                $.toptips('图片存储失败');
            }
        }).error(function(){
            $.toptips('服务器错误');
        });*/
    });
});
