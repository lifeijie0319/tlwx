$(function(){
    var firstrow = 0;
    var lastrow = 4;
    var nextpage = true;
    var loading = false;
    var load_num = 4;
    function load(){
        data = JSON.stringify({
            'firstrow': firstrow,
            'lastrow': lastrow,
        });
        if(loading) return false;
        loading = true;
        $("#loading").html('<i class="ys_loading"></i><span class="ys_more_tips">正在加载</span>');
        $.post(BASE_URL + '/ccrd/bill', data, function(resp){
            $('#bill_detail').append(resp.html);
            firstrow = lastrow + 1;
            lastrow = firstrow + load_num;
            nextpage = resp.nextpage;
            if(resp.nextpage){
                $("#loading").html('<span class="ys_more_tips">下拉加载更多</span>');
            }else{
                $("#loading").html("<span class='ys_more_tips'>无更多记录</span>");
            }
            loading = false;
        });
    }
    $('#tab2_btn').on('click', function(){
        load(firstrow, lastrow);
    });
    $(window).on('touchmove', function(){
        var scrollTop = $(this).scrollTop();               //滚动条距离顶部的高度
        var scrollHeight = $(document).height();           //当前页面的总高度
        var windowHeight = $(this).height();               //当前可视的页面高度
        if(scrollTop + windowHeight >= scrollHeight && nextpage){        //距离顶部+当前高度 >=文档总高度 即代表滑动到底部
            load();
        }
    });
});
