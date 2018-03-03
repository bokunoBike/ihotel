$('#myModal').on('show.bs.modal', function () {
	document.getElementsByTagName('body')[0].style.paddingTop='0';
	document.getElementById('navbarContainer').style.position='static';
	document.getElementById('navbarContainer').style.padding='0';
})
$('#myModal').on('hidden.bs.modal', function () {
	document.getElementsByTagName('body')[0].style.paddingTop='60px';
  document.getElementById('navbarContainer').style.position='fixed';
})
