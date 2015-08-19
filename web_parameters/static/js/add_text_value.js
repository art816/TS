$(document).ready(function(){
	$("input").click(function(){ 
        $.getJSON(url_for('show_param', param_name=$(this).parent().previuos().previos().id()), function(data) {
        console.log('showNumberOfEntries:', data.param);
	    $("dd [name='fullname']").attr({value: '1'});
        console.log("sdfadfasdf");
	});
});
