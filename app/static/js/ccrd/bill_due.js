$(function(){
    var firstrow = 0;
    var lastrow = 6;
    var nextpage = true;
    var loading = false;
    var load_num = 6;
    function load(){
        data = JSON.stringify({
            'firstrow': firstrow,
            'lastrow': lastrow,
        });
        if(loading) return false;
        loading = true;
        $("#loading").html('<i class="ys_loading"></i><span class="ys_more_tips">正在加载</span>');
        $.post(BASE_URL + '/ccrd/bill_due', data, function(resp){
            if(resp.success){
                $('#content').append(resp.html);
                firstrow = lastrow + 1;
                lastrow = firstrow + load_num;
                nextpage = resp.nextpage;
                if(resp.nextpage){
                    $("#loading").html('<span class="ys_more_tips">下拉加载更多</span>');
                }else{
                    $("#loading").html("<span class='ys_more_tips'>无更多记录</span>");
                }
            }else{
                $("#loading").html('<span class="ys_more_tips">' + resp.msg + '</span>');
            }
            loading = false;
        });
    }
    load(firstrow, lastrow)
    $(window).on('scroll', function(){
        var scrollTop = $(this).scrollTop();               //滚动条距离顶部的高度
        var scrollHeight = $(document).height();           //当前页面的总高度
        var windowHeight = $(this).height();               //当前可视的页面高度
        console.log(scrollTop + windowHeight, scrollHeight, nextpage);
        if(scrollTop + windowHeight + 1 >= scrollHeight && nextpage){        //距离顶部+当前高度 >=文档总高度 即代表滑动到底部
            load();
        }
    });
});
