getRandomArbitrary = function (min, max) {
    return Math.random() * (max - min) + min;
}

scrol = function() {
    //if($("#checkbox").prop("checked")){
        $("#warning").css({visibility: 'visible'})
		var offset = $("#warning").offset();
        console.log('offset', offset);
		var topPadding = 5;
        var curr_opacity = $("#warning").css("opacity");
		$(window).scroll(function() {
			if ($(window).scrollTop()) {
				$("#warning").stop().animate({marginTop: $(window).scrollTop() + topPadding});
			}
			else {$("#warning").stop().animate({marginTop: 0});};});
        curr_opacity = getRandomArbitrary(0.8,1);
        $("#warning").css({opacity: curr_opacity});
    //}
    //else{
    //    $("#warning").css({visibility:'hidden'});
    //}
	};

$(window).ready(scrol);
