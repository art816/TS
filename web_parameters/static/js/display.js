$(document).ready(function(){
	$("div.title").click(function(){
		$(this).next("div.sub_title").slideToggle();
	});
});

