windowsHeight = document.documentElement.clientHeight;
totalHeight=document.getElementById("none").offsetTop;
if(totalHeight<windowsHeight)
{
  colHeight = windowsHeight-document.getElementById("footer").offsetTop;
  document.getElementById("footer").style.height=colHeight+"px";
}
$(document).ready(function(){
  $(window).resize(function(){
    location.reload();
  });
});
