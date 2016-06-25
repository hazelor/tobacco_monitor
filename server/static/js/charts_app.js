


function render_chart(datas,chart_title,unit,plot_type,chart_id){
    Highcharts.setOptions({
            global: {
                useUTC: false
            }
        });

    $('#'+chart_id).highcharts({
        chart: {
                type: plot_type,                      //曲线样式
                animation: Highcharts.svg, // don't animate in old IE
                marginRight: 10,
            },
            title:{
                text:chart_title
            },

            xAxis: {
                type: 'datetime',
                minRange:60*60*1000
                //minRange:60*1000

            },
            yAxis: {
                title: {
                    text: unit
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
                enabled: true
            },
            series: datas,//format [{name: "name", data: [[x1,y1],[x2,y2]]},{name: "name", data:[[x1,y1],[x2,y2]]}]
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
