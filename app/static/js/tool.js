var BASE_URL = 'https://hz.wx.yinsho.com/tlwx';
var APPID = 'wx6290daffb81416ac';
//APPID = 'wx64a1fdc74458e608';

function getClientType(){
    var u = navigator.userAgent;
    if(u.indexOf('Android') > -1 || u.indexOf('Linux') > -1){
        return 'android';
    }else if(!!u.match(/\(i[^;]+;( U;)? CPU.+Mac OS X/)){
        return 'ios';
    }else{
        return 'others';
    }
}

function rd(n,m){
    var c = m-n+1;  
    return Math.floor(Math.random() * c + n);
}

function getUrlArgs(name, query=window.location.search) { 
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i"); 
    var r = query.substr(1).match(reg); 
    if (r != null) return unescape(r[2]); return null; 
}

function sendVcode(sendBtn, telephoneInputEle) {
    //alert('enter send_vcode');
    //alert('disabled:', sendBtn.prop('disabled'));
    console.log(sendBtn.prop('disabled'));
    if(sendBtn.prop('disabled')) return false;
    telValidateRes = $.cell_validate(telephoneInputEle);
    if(telValidateRes == 'empty'){
        $.toptips('发送验证码之前请输入手机号!');
        return false;
    }else if(telValidateRes == 'notMatch'){
        return false;
    }else{
        $.post(BASE_URL + '/common/send_vcode', telephoneInputEle.val(), function (resp) {
            $.toptips("验证码已发送，请查收！", 'success');
        });
    };
    var times = 60;
    sendBtn.prop('disabled', true);
    console.log(sendBtn.prop('disabled'));
    timer = setInterval(function () {
        times--;
        sendBtn.text(times + "秒后重试");
        if (times <= 0) {
            sendBtn.text("发送验证码");
            sendBtn.prop('disabled', false);
            console.log(sendBtn.prop('disabled'));
            clearInterval(timer);
            times = 60;
        }
    }, 1000);
}

function configJssdk(apilist){
    $.post(BASE_URL + '/wx/jssdk', {url: window.location.href}, function(resp){
        if(resp.success){
            resp = resp.config;
            wx.config({
                debug : false,
                appId : APPID,
                timestamp : resp.timestamp,
                nonceStr : resp.nonceStr,
                signature : resp.signature,
                jsApiList : apilist,
            });
        }else{
            console.log(resp.msg);
        }
    }).error(function(xhr, textStatus, errorThrown){
        alert(xhr.status);
        alert(xhr.readyState);
        alert(textStatus);
    });
}

function wxUploadImg(img_dom, source_type=['album']){
    wx.chooseImage({
        count: 1, // 默认9
        sizeType: ['original', 'compressed'], // 可以指定是原图还是压缩图，默认二者都有
        sourceType: source_type, // 可以指定来源是相册还是相机，默认二者都有
        success: function (res) {
            var localIds = res.localIds // 返回选定照片的本地ID列表，localId可以作为img标签的src属性显示图片
            if(getClientType() == 'ios'){
                //alert('ios');
                wx.getLocalImgData({
                    localId: localIds[0],
                    success: function(res){
                        img_dom.attr('src', res.localData);
                        //alert(res.localData);
                    },
                    fail: function(){
                        alert('该图片暂时无法预览');
                    }
                });
            }else{
                img_dom.attr('src', localIds[0]);
            }
            wx.uploadImage({
                localId: localIds[0], // 需要上传的图片的本地ID，由chooseImage接口获得
                isShowProgressTips: 1, // 默认为1，显示进度提示
                success: function(res){
                    var serverId = res.serverId; // 返回图片的服务器端ID
                    img_dom.attr('mediaid', serverId);
                }
            });
        }
    });
}

//serialize form
+ function($) {
    $.fn.serializeForm= function(){
        var o = {};
        var a = this.serializeArray();
        //console.log(a);
        $.each(a, function() {
            if (o[this.name] !== undefined) {
                if (!o[this.name].push) {
                    o[this.name] = [o[this.name]];
                }
                o[this.name].push(this.value || '');
            } else {
                o[this.name] = this.value || '';
            }
        });
        return JSON.stringify(o);
    }
}($);
