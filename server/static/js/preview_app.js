/**
 * Created by guoxiao on 16/2/27.
 */
var sign;
function on_selected_device_change(){
    //render_chart([[],[]])
    var date = new Date()
    var end_time = date.pattern("yyyy-MM-dd hh:mm");
    var date_milliseconds = date.getTime();
    date_milliseconds -= 1000*60*19;
    date = new Date(date_milliseconds);
    var start_time = date.pattern("yyyy-MM-dd hh:mm");
    //var chart = $('#container').highcharts()
    //var series = chart.series;
    //series[0].remove(false)
    //series[1].remove(false)
    if(sign){
        clearInterval(sign)
    }

    if ($('#selected_device').children('option:selected').val() != ''){
        //var title = {
        //    text:$('#chamber_name').children('option:selected').text()
        //}
        //var chart = new Highcharts.Chart()
        //chart.setTitle(title)
        loading_begin('数据准备中')
        //alert('--------test--------')
        $.ajax({
                url:'history/query',
                type:'GET',
                timeout: 2000,
                dataType:'text',
                data:{'dev_id':$('#selected_device').children('option:selected').attr('value'),
                      'start_time':start_time,
                      'end_time':end_time
                      },
                success:function(data, status){
                    if(data==''){
                        //alert('所选择的时间段没有数据!')
                        loading_end();
                    }
                    else{
                        var jdata= $.parseJSON(data);
                        if(jdata.length >0){
                            for(var i = 0;i<jdata.length;i++){
                            render_chart(jdata[i]['values'],jdata[i]['name'],jdata[i]['name'], 'chart_'+jdata[i]['type_id'])
                            }
                        }
                    }

                        loading_end()
                    },
                error:function(jqXHR, textStatus, errorThrown){
                    loading_end();
                }
            })
        sign=setInterval(
            function(){
                $.ajax({
                    url:'preview/realtime',
                    type:'get',
                    dataType:'text',
                    timeout: 1800,
                    data:{'sel_device_id':$('#selected_device').children('option:selected').attr('value'),
                         },
                    success:function(data, status){
                        var data = $.parseJSON(data);
                        var current_date = data['date'];
                        var data_content = data['content'];
                        if(data_content){
                            var innerHTML_str = '<colgroup><col class="col-xs-1"><col class="col-xs-3"></colgroup><thead><tr><th>项目</th><th>信息</th></tr></thead>';
                            for(var i =0; i<data_content.length;i++){
                                var chart = $('#chart_'+data_content[i]['type_id']).highcharts();
                                var series = chart.series;
                                serie_1_len = series[0].data.length;
                                if(serie_1_len != 0){
                                    var plot_data = [current_date, data_content[i]['value']];
                                    if(series[0].data[serie_1_len-1]['x'] != plot_data[0]){
                                        if(plot_data[0]-series[0].data[0]['x']>=20*60*1000){
                                            series[0].addPoint(plot_data,true,true)
                                        }
                                        else{
                                            series[0].addPoint(plot_data,true,false)
                                        }
                                    }
                                }
                                var value = parseFloat(data_content[i]['value']);
                                value = value.toFixed(2);
                                innerHTML_str = innerHTML_str + '<tr>'+'<td>'+data_content[i]['name']+'</td>'+'<td>'+value+'</td>'+'</tr>'

                            }
                            document.getElementById('data_table').innerHTML = innerHTML_str;


                        }
                    }
                })
            },2000
        )
    }
}

$(function(){
    var opts = {
      lines: 12,            // The number of lines to draw
      length: 7,            // The length of each line
      width: 5,             // The line thickness
      radius: 10,           // The radius of the inner circle
      scale: 1.0,           // Scales overall size of the spinner
      corners: 1,           // Roundness (0..1)
      color: '#000',        // #rgb or #rrggbb
      opacity: 1/4,         // Opacity of the lines
      rotate: 0,            // Rotation offset
      direction: 1,         // 1: clockwise, -1: counterclockwise
      speed: 1,             // Rounds per second
      trail: 100,           // Afterglow percentage
      fps: 20,              // Frames per second when using setTimeout()
      zIndex: 2e9,          // Use a high z-index by default
      className: 'spinner', // CSS class to assign to the element
      top: '100px',           // center vertically
      left: '50%',          // center horizontally
      shadow: false,        // Whether to render a shadow
      hwaccel: false,       // Whether to use hardware acceleration (might be buggy)
      position: 'absolute'  // Element positioning
    };
    var target = document.getElementsByClassName('LoadingImg');
    //alert(target)
    //var spinner = new Spinner(opts).spin(target);
    var spinner = new Spinner().spin(target[0]);
    //$(function(){
    //    render_chart()
    //    });
    on_selected_device_change()
});


function loading_begin(loading_message){
    $(".LoadingBg").height(document.body.clientWidth);
    $(".LoadingBg").show();
    $(".LoadingImg").fadeIn(300);
    $(".Loading_message").html("<p>"+loading_message+"</p>");
    $(".Loading_message").fadeIn(300)

}
function loading_end(){
    $('.LoadingBg, .LoadingImg, .Loading_message').hide();
}



function render_chart(datas, title, title_y, type_id){
    Highcharts.setOptions({
            global: {
                useUTC: false
            }
        });

        $('#'+type_id).highcharts({
            chart: {

                type: 'spline',                      //曲线样式
                animation: Highcharts.svg, // don't animate in old IE
                marginRight: 10,
            },
            title:{
                text:title
            },

            xAxis: {
                type: 'datetime',
                minRange:60*60*1000
                //minRange:60*1000

            },
            yAxis: {
                title: {
                    text: title_y
                },
                plotLines: [{
                    value: 0,
                    width: 1,
                    color:'blue'
                    //color: '#808080'
                }]
            },
            tooltip: {
                backgroundColor:'#fff',
                borderColor:'black',
                formatter: function () {        //数据提示框中单个点的格式化函数
                    return '<b>' + this.series.name+ '</b><br/>' +
                        Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' +
                        Highcharts.numberFormat(this.y, 3);   //小数后几位
                }
            },
            legend: {
                enabled: true
            },
            exporting: {
                enabled: false
            },
            series: [
                {
                    name: title,
                    data:datas
                }]
        })
}

Date.prototype.pattern=function(fmt) {
    var o = {
    "M+" : this.getMonth()+1, //月份
    "d+" : this.getDate(), //日
    "h+" : this.getHours(), //小时
    "H+" : this.getHours(), //小时
    "m+" : this.getMinutes(), //分
    "s+" : this.getSeconds(), //秒
    "q+" : Math.floor((this.getMonth()+3)/3), //季度
    "S" : this.getMilliseconds() //毫秒
    };
    var week = {
    "0" : "/u65e5",
    "1" : "/u4e00",
    "2" : "/u4e8c",
    "3" : "/u4e09",
    "4" : "/u56db",
    "5" : "/u4e94",
    "6" : "/u516d"
    };
    if(/(y+)/.test(fmt)){
        fmt=fmt.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length));
    }
    if(/(E+)/.test(fmt)){
        fmt=fmt.replace(RegExp.$1, ((RegExp.$1.length>1) ? (RegExp.$1.length>2 ? "/u661f/u671f" : "/u5468") : "")+week[this.getDay()+""]);
    }
    for(var k in o){
        if(new RegExp("("+ k +")").test(fmt)){
            fmt = fmt.replace(RegExp.$1, (RegExp.$1.length==1) ? (o[k]) : (("00"+ o[k]).substr((""+ o[k]).length)));
        }
    }
    return fmt;
}
