var myChart = null;
var node = null;
var url = window.location.href.split('/');
var host = window.location.hostname;
var expireHour;
var expireMinute;
var expireSecond;
if(url[4] != 'adminCertainRoom')
{
	myChart = echarts.init(document.getElementById('showChart'),'dark');
}
window.onload = initWindow();
function initWindow()
{
	getPersonNumber();
	getExpireTime();
}
//通过webSocket获取系统判定人数
function getPersonNumber()
{
	var ws = new WebSocket("ws://"+host+":8000/user/get_room_info");
	window.ws = ws;
	ws.onmessage = function (e)
	{
		var data = JSON.parse(e.data);
		systemPersonNumber = data.people_counts;
		console.log(systemPersonNumber);
		if(url[4] == 'adminCertainRoom')
		{
			document.getElementById('number').innerHTML = systemPersonNumber;
		}
		console.log("onmessage");
		var now = new Date();
		var nowHour = now.getHours();
		var nowMinute = now.getMinutes();
		var nowSecond = now.getSeconds();
		if(((expireHour-nowHour)*60*60+(expireMinute-nowMinute)*60+expireSecond-nowSecond) <= 0&&systemPersonNumber == 0&&url[4] != 'adminCertainRoom')
		{
			document.getElementById('showChart').style.boxShadow = 'none';
		}
		//console.log(systemPersonNumber);
	}
	ws.onopen = function()
	{
		console.log("onopen");
	}
	ws.onclose = function()
	{
		getPersonNumber();
		ws.send(0);
	}
	ws.onerror = function(e)
	{
		ws.send(0);
	}
}
//获得过期时间
function getExpireTime()
{
	//获取过期时间初始化计时器
	$.ajax({
		type: 'GET',
		url:'http://' + host + ':8000/user/get_expire_time',
		dataType: 'json',
		// 下面两个参数解决跨域问题
		xhrFields: {
				withCredentials: true
		},
		crossDomain: true,
		complete: function(XMLHttpRequest, textStatus) {},
		success: function(data)
		{
			var expireTime = new Date(data.expire_time);
			expireHour = expireTime.getHours();
			expireMinute = expireTime.getMinutes();
			expireSecond = expireTime.getSeconds();
			console.log(expireHour*60*60+expireMinute*60+expireSecond);
		},
		error: function(err) {
			console.log(err);
		}
	});
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
function addPerson()
{
	clickChange = true;
	nowPerson = document.getElementById('number').innerHTML;
	changeNumber = Number(nowPerson)+1;
	document.getElementById('number').innerHTML = changeNumber;
}
//点击减少人数
function subPerson()
{
	clickChange = true;
	nowPerson = document.getElementById('number').innerHTML;
	changeNumber = Number(nowPerson)-1;
	if(changeNumber >=0)
	{
		document.getElementById('number').innerHTML = changeNumber;
	}
}
//修改人数
function sendModify()
{
	document.getElementById('feedback').style.display = 'block';
}

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
for (var i = 0; i < 60; i++) {
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
