var myChart = null;
var node = null;
var url = window.location.href.split('/');

if(url[4] != 'adminCertainRoom')
{
	myChart = echarts.init(document.getElementById('showChart'),'dark');
}
//点击显示大图表
$("canvas").click(function()
{
	console.log('hhh');
});
function showBigChart()
{
	window.location.href = "/admin/adminCertainRoom";
}
//返回多图表界面
function returntoCharts()
{
	document.getElementById('feedback').style.display = 'none';
	var width =  window.screen.width;
	console.log(width);
	if(width < 768)
	{
		window.location.href = "/admin/adminCertainRoom";
	}
	else
	{
		window.location.href = "/admin";
	}
}

//监控标签页的打开和隐藏
document.addEventListener('webkitvisibilitychange',function()
			 {
					 if(document.webkitVisibilityState=='hidden')
					 {}
					 else
					 {
							 //$.ajax(getting);
					 }
			 })
document.addEventListener('mozvisibilitychange',function()
			 {
					 if(document.mozVisibilityState=='hidden')
					 {}
					 else
					 {
							 //$.ajax(getting);
					 }
			 })

//获取随机数据
function randomData() {
    now = new Date(+now + 1000);
    var year=now.getFullYear();
    var month=now.getMonth()+1;
    var day=now.getDate();
    var hour=now.getHours();
    var minute=now.getMinutes();
    var second=now.getSeconds();
    value = value + Math.random() * 21 - 10;
    return {
        name: now.toString(),
        value: [
            year+'/'+month+'/'+day+' '+hour+':'+minute+':'+second,
            Math.round(value)
        ]
    }
}

var data = [];
var now = new Date()-17*60*1000;
var oneDay = 24 * 3600 * 1000;
var value = Math.random() * 1000;
for (var i = 0; i < 50; i++) {
    data.push(randomData());
}

option = {
    title: {
        text: '传感器输出信号',
        textStyle: {
               fontWeight: 'normal',              //标题颜色
               //color: 'gray'
           },
    },
    tooltip: {
        trigger: 'axis',
        formatter: function (params) {
            params = params[0];
            var date = new Date(params.name);
            return date.getHours() + ':' + date.getMinutes() + ':' + date.getSeconds() + ' value: ' + params.value[1];;
        },
        axisPointer: {
            animation: false
        }
    },
    xAxis: {
        type: 'time',
        splitLine: {
            show: false
        }
    },
    yAxis: {
        type: 'value',
        boundaryGap: [0, '100%'],
        splitLine: {
            show: false
        }
    },
    backgroundColor:'#303030',
    series: [{
        smooth:true,
        name: '模拟数据',
        type: 'line',
        showSymbol: false,
        hoverAnimation: false,
        data: data
    }]
};

setInterval(function () {

    for (var i = 0; i < 1; i++) {
      //myChart.clear();
        data.shift();
        data.push(randomData());
    }

    myChart.setOption(option);
}, 1000);
//显示楼层号输入
function showForm()
{
	var windowWidth=document.documentElement.clientWidth;
	if(windowWidth<768)
	{
		document.getElementById('form').style.display="block";
		document.getElementById('main-window').style.display="none";
		document.getElementById('changeFloor').style.display="none";
	}
}
$(document).ready(function(){
  $('#submitButton').click(function(){
    var windowWidth=document.documentElement.clientWidth;
    if(windowWidth<768)
    {
      document.getElementById('form').style.display="none";
      document.getElementById('main-window').style.display="block";
    }
  });
});
