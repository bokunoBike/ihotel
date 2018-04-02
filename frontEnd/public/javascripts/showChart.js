var myChart = null;
var node = null;
var url = window.location.href.split('/');
var host = window.location.hostname;
var senor;//传感器信号list

window.onload = initWindow();
function initWindow()
{
	getPersonNumber();
	getExpireTime();
	if(url[4] != 'adminCertainRoom')
	{
		myChart = echarts.init(document.getElementById('showChart'),'dark');
	}
	getSenor();
}
//通过webSocket获取系统判定人数
function getPersonNumber()
{
	var ws = new WebSocket("ws://"+host+":8000/manager/get_room_people_counts_and_pattern?room_id=Z101");
	window.ws = ws;
	ws.onmessage = function (e)
	{
		var data = JSON.parse(e.data);
		systemPersonNumber = data.people_counts;
		var pattern = data.pattern;
		//console.log("pattern"+pattern);
		if(pattern == false&&systemPersonNumber == 0)
		{
			//console.log("lightOff");
			if(url[4] != 'adminCertainRoom')
			{
				document.getElementById('showChart').style.boxShadow = 'none';
			}
			else
			{
				document.getElementById('main-window').style.boxShadow = 'none';
			}
		}
		else
		{
			//console.log("lightOn");
			if(url[4] != 'adminCertainRoom')
			{
				document.getElementById('showChart').style.boxShadow = '0 0 20px #E2C08D';
			}
			else
			{
				document.getElementById('main-window').style.boxShadow = '0 0 20px #E2C08D';
			}
		}
		//console.log(systemPersonNumber);
	}
	ws.onclose = function()
	{
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
		},
		error: function(err) {
			console.log(err);
		}
	});
}
//设置楼层提示信息
function changeFloorClick()
{
	var floorNumber = document.getElementById('inputFloor').value;
	if(!isNaN(floorNumber)&&floorNumber <= 10&&floorNumber > 0&&floorNumber != '')
	{
		document.getElementById('floorNumber').innerHTML = floorNumber;
		document.getElementById('justifyNotice').style.display = "none";
	}
	else
	{
		document.getElementById('justifyNotice').style.display = "block";
	}
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
/*function randomData() {
    now = new Date(+now + 1000);
    var year=now.getFullYear();
    var month=now.getMonth()+1;
    var day=now.getDate();
    var hour=now.getHours();
    var minute=now.getMinutes();
    var second=now.getSeconds();
    value = value + Math.random() * 21 - 10;
    return {
        //name: now.toString(),
        value: [
            year+'/'+month+'/'+day+' '+hour+':'+minute+':'+second,
            Math.round(value)
        ]
    }
}*/
//获取传感器信号
function getSenor()
{
	var ws = new WebSocket("ws://"+host+":8000/manager/get_room_signal");
	window.ws = ws;
	var times = 0;
	ws.onmessage = function (e)
	{
		var data = JSON.parse(e.data);
		//myChart.clear();
		now = new Date();
		now = new Date(+now-1000);
		/*dataUltrasound1.splice(0,dataUltrasound1.length);
		dataUltrasound2.splice(0,dataUltrasound2.length);*/
		if(times == 0)
		{
			now = new Date(+now-4000);
			for(var i = 0;i < 40;i++)
			{
				var senorValue1 = {
						name: now.toString(),
						value: [
								now,
								0
						]
				}
				var senorValue2 = {
						name: now.toString(),
						value: [
								now,
								0
						]
				}
				now = new Date(+now+100);
				dataUltrasound1.push(senorValue1);
				dataUltrasound2.push(senorValue2);
			}
		}
		for(var i = 0;i < 10;i++)
		{
			dataUltrasound1.shift();
			dataUltrasound2.shift();
		}

		for (var i = 0; i < 10; i++)
		{
			var senorValue1 = {
					name: now.toString(),
					value: [
							now,
							data.signal1[i]
					]
			}
			var senorValue2 = {
					name: now.toString(),
					value: [
							now,
							data.signal2[i]
					]
			}
			now = new Date(+now+100);
			dataUltrasound1.push(senorValue1);
			dataUltrasound2.push(senorValue2);
		    //data.push(randomData())
		}
		myChart.setOption(option);
		window.onresize = myChart.resize;
		times++;
	}
	ws.onclose = function()
	{
		ws.send(0);
	}
	ws.onerror = function(e)
	{
		ws.send(0);
	}
}

var dataUltrasound1 = [];
var dataUltrasound2 = [];
var dataInfared1 = [];
var dataInfared2 = [];


option = {
    title: {
        text: 'Z101传感器信号',
        textStyle: {
               fontWeight: 'normal'              //标题颜色
               //color: 'gray'
           }
    },
    tooltip: {
        trigger: 'axis',
        formatter: function (params) {
					var date = new Date(params[0].name);
					var res = '时间: '+date.getHours() + ':' + date.getMinutes() + ':' + date.getSeconds();
					for(var i=0;i<params.length;i++)
					{
						res+='<p>'+params[i].seriesName+': '+params[i].value[1]+'</p>'
					}
					return res;
        },
        axisPointer: {
            animation: false
        }
    },
		legend: {
							 data:['超声1','超声2'],
							 right:0,
							 top:10,
							 orient: 'vertical'
					 },
    xAxis: {
        type: 'time',
        splitLine: {
            show: false
        },
				axisLabel:{interval: 0}
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
        //smooth:true,
        name: '超声1',
        type: 'line',
        showSymbol: false,
        hoverAnimation: true,
        data: dataUltrasound1
    },
		{
			//smooth:true,
			name: '超声2',
			type: 'line',
			showSymbol: false,
			hoverAnimation: true,
			data: dataUltrasound2
		}/*,
		{
			smooth:true,
			name: '红外1',
			type: 'line',
			showSymbol: false,
			hoverAnimation: false,
			data: dataInfared1
		},
		{
			smooth:true,
			name: '红外2',
			type: 'line',
			showSymbol: false,
			hoverAnimation: false,
			data: dataInfared2
		}*/
	]
};

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
