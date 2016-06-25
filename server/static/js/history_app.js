/**
 * Created by guoxiao on 16-6-3.
 */

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

window.onload=function(){
    var date = new Date()
    document.getElementById('end_time').value = date.pattern("yyyy-MM-dd hh:mm")
    var date_milliseconds = date.getTime()
    date_milliseconds -= 1000*60*60*24
    date = new Date(date_milliseconds)
    document.getElementById('start_time').value = date.pattern("yyyy-MM-dd hh:mm")



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
}

function loading_begin(loading_message){
    $(".LoadingBg").height(document.body.clientWidth);
    $(".LoadingBg").show();
    $(".LoadingImg").fadeIn(300);
    $(".Loading_message").html("<p>"+loading_message+"</p>")
    $(".Loading_message").fadeIn(300)

}
function loading_end(){
    $('.LoadingBg, .LoadingImg, .Loading_message').hide();
}



function render_chart(datas, title, title_y, plot_type){
    Highcharts.setOptions({
            global: {
                useUTC: false
            }
        });

        $('#chart_history').highcharts({
            chart: {
                type: plot_type,                      //曲线样式
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


$(function(){
    render_chart([],'','','spline')
        });


function selected_history(){
    //alert(document.getElementById('start_time').value)
    var start_time_str = document.getElementById('start_time').value;
    if(start_time_str == ''){
        alert('请输入有效起始时间')
        return
    }
    var end_time_str = document.getElementById('end_time').value;
    if(end_time_str == ''){
        alert('请输入有效结束时间')
        return
    }
    var start_str = (start_time_str+":00").replace(/-/g,"/")
    var start_date = new Date(start_str)
    var end_str = (end_time_str+":00").replace(/-/g,"/")
    var end_date = new Date(end_str)
    if(end_date-start_date>86400000){
//        alert(end_date-start_date)
        alert('所选时间间隔大于24小时!')
        return
    }
    var count = Math.floor((end_date-start_date)/2880000)


    loading_begin('数据准备中')
    //alert('--------test--------')
    var historyDataRequest=$.ajax({
        url:'history/query',
        timeout:30000,
        type:'GET',
        dataType:'text',
        data:{'dev_id':$('#sel_device').children('option:selected').attr('value'),
              'type_id':$('#sel_data').children('option:selected').attr('value'),
              'start_time':document.getElementById('start_time').value,
              'end_time':document.getElementById('end_time').value
              },
        success:function(data, status){
            if(data==''){
                alert('所选择的时间段没有数据!');
                loading_end();
            }
            else{
                var jdata= $.parseJSON(data)
                var datas = new Array();
                for (var i=0;i<jdata['values'].length;i++){
                    //if(i%count==0){
                        datas.push(jdata['values'][i]);
                    //}
                }
                if(jdata['duration'] == 0){
                    render_chart(datas, jdata['name'], jdata['unit'],'spline');
                }
                else {
                    render_chart(datas, jdata['name'], jdata['unit'],'column');
                }


                loading_end()
            }

        },
        complete:function(XMLHttpRequest,status){
            if(status=='timeout'){
                historyDataRequest.abort();
                loading_end();
            }
            else{
                loading_end();
            }
        }
    })
}



function device_changed(){
    var sel_device_id = document.getElementById("sel_device").value;
    $.ajax({
        url:'/data/history',
        type:'post',
        data:{'dev_id': sel_device_id},
        success:function(data, status){
            data_list = JSON.parse(data)
            $("#sel_data option").remove();
            for(i=0;i<data_list.length;i++){
                //alert("<option value="+"'"+data_list[i][0]+"'"+">"+data_list[i][1]+"</option>")
                $("#sel_data").append("<option value="+data_list[i]['type_id']+">"+data_list[i]['name']+"</option>");
            }

        }
    })

}

