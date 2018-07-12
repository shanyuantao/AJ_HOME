function hrefBack() {
    history.go(-1);
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function(){
   var path = location.search;
   // /house/detail/?id=x
   id = path.split('=')[1];
   $.get('/house/detail/' + id + '/', function (data) {
       if (data.code == '200'){

           // 异步把数据传入页面 house_detail_list是script的id

           var detail_house = template('house_detail_list', {ohouse: data.house, facilitys: data.facility_list});
           // 把上面的模板加入这个类标签里 {% raw %}标签中可以使用传入的数据
           $('.container').append(detail_house);

           // 对 class = swiper-container div标签中的图片做轮播
           var mySwiper = new Swiper('.swiper-container', {
               loop: true,
               // 自动轮播时间2秒
               autoplay: 2000,
               // 可以左右翻 Interaction交互、互动的意思
               autoplayDisableOnInteraction: false,
               // pageination 页码； 页面显示 是 class = swiper-pagination的div标签
               pagination: '.swiper-pagination',
               // 以分数的形式显示页码 2 / 3, 当前第二页， 共3页
               paginationType: 'fraction'
           });
           // 展示即刻预定按钮
           $('.book-house').show();
       }
   })
});