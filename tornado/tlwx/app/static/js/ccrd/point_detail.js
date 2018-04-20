$(function(){
    var firstrow = 0;
    var lastrow = 4;
    var nextpage = true;
    var loading = false;
    function load(start=null, end=null){
        data = JSON.stringify({
            'firstrow': firstrow,
            'lastrow': lastrow,
            'start': start,
            'end': end
        });
        if(loading) return false;
        loading = true;
        $("#loading").html('<i class="ys_loading"></i><span class="ys_more_tips">正在加载</span>');
        $.post(BASE_URL + '/ccrd/bill_due', data, function(resp){
            $("#content").append(resp.html);
            nextpage = resp.nextpage;
            if(resp.nextpage){
                $("#loading").html('<span class= "ys_more_tips">下拉加载更多</span>');
            }else{
                $("#loading").html("<span class = 'ys_more_tips'>无更多记录</span>");
            }
            loading = false;
        });
    }
    load();
    $(window).on('touchmove', function(){
        var scrollTop = $(this).scrollTop();               //滚动条距离顶部的高度
        var scrollHeight = $(document).height();           //当前页面的总高度
        var windowHeight = $(this).height();               //当前可视的页面高度
        if(scrollTop + windowHeight >= scrollHeight && nextpage){        //距离顶部+当前高度 >=文档总高度 即代表滑动到底部
            load();
        }
    });
    $('#submit').on('click', function(){
        start_date = $('input[name="start_date"]').val();
        end_date = $('input[name="end_date"]').val();
        if(start_date > end_date){
            $.toptips('起始日期大于截止日期');
        }
        firstrow = 0;
        lastrow = 4;
        nextpage = true;
        $('#content').empty();
        load(start_date, end_date);
    });
});
