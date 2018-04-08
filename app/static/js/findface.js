$(function(){
    $('#upload').on('click', function(){
        formdata = new FormData();
        img = $('#face')[0].files[0];
        console.log(img);
        formdata.append('photo', img);
        formdata.append('dirname', 'face');
        $.toptips('正在上传', 'success');
        $.ajax({
            url: BASE_URL + '/common/upload_img',
            type: 'post',
            contentType: false,
            processData: false,
            data: formdata,
            success: function(resp){
                if(resp.success){
                    $.toptips('上传成功', 'success');
                }else{
                    $.toptips('上传失败');
                }
            },
            error: function(){
                $.toptips('服务器错误');
            }
        });
    });
    $('#detect').on('click', function(){
        api_url = 'http://jswj888.f3322.net:8889';
        formdata = new FormData();
        img = $('#face')[0].files[0];
        console.log(img);
        formdata.append('photo', img);
        $.ajax({
            url: api_url + '/n-tech/v0/detect',
            type: 'post',
            headers: {'Authorization': 'Token tGd3-nXYt'},
            contentType: false,
            processData: false,
            data: formdata,
            success: function(resp){
                console.log(resp);
            },
            error: function(){
                console.log('error');
            }
        }); 
    });
});
