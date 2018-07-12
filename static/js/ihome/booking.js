function hrefBack() {
    history.go(-1);
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

function showErrorMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

$(document).ready(function(){
    $(".input-daterange").datepicker({
        format: "yyyy-mm-dd",
        startDate: "today",
        language: "zh-CN",
        autoclose: true
    });
    $(".input-daterange").on("changeDate", function(){
        var startDate = $("#start-date").val();
        var endDate = $("#end-date").val();

        if (startDate && endDate && startDate > endDate) {
            showErrorMsg();
        } else {
            var sd = new Date(startDate);
            var ed = new Date(endDate);
            days = (ed - sd)/(1000*3600*24) + 1;
            var price = $(".house-text>p>span").html();
            var amount = days * parseFloat(price);
            $(".order-amount>span").html(amount.toFixed(2) + "(共"+ days +"晚)");
        }
    });
});
// 只有这个是自己写的
$(document).ready(function () {
    // 转换下入住时间的格式

    $('.input-daterange').datepicker({
        format: 'yyyy-mmmm-dd',
        startDate: 'today',
        language: 'zh-CN',
        autoclose: true
    });

    // 根据入住天数 和 房间的单价 计算总价
    $('.input-daterange').on('changeDate', function () {
        var startDate = $("#start-date").val();
        var endDate = $("#end-date").val();

        if (startDate && endDate && startDate > endDate) {
            showErrorMsg()
        }else{
            var sd = new Date(startDate);
            var ed = new Date(endDate);
            days = (ed - sd)/(1000*3600*24) + 1;
            var price = $(".house-text>p>span").html();
            var amount = days * parseFloat(price);
            $(".order-amount>span").html(amount.toFixed(2) + "(共" + days + "晚)");
        }
    });


    // 传递参数但是可以不接，依然跳转到对应的绝对路径
    var path = location.search;
    id = path.split('=')[1];
    
    $.get('/house/detail/' + id + '/', function (data) {
        alert(data.code);
        if (data.code == '200'){
            // house_booking 是script标签的id属性
            var house_booking = template('house_booking', {ohouse: data.house});
            // 往这个标签中填充内容
            $('.house-info').html(house_booking)
        }
        
    });

    // 点击提交按钮时进行的操作， 保存数据， 跳转到订单页面
    $('.submit-btn').click(function(){

        var path = location.search;
        id = path.split('=')[1];
        
        var start_date = $('#start-date').val();
        var end_date = $('#end-date').val();
        $.post('/order/', {house_id: id, start_time: start_date, end_time: end_date},
            function (data) {
                if (data.code == '200'){
                    alert('11111111111');
                    // 跳转到我的订单页面
                    location.href = '/order/order/';
                }
            });
    });
});
