updateInerval = 1 * 1000;  // ms

getRandomArbitrary = function (min, max) {
    return Math.random() * (max - min) + min;
}

showNumberOfEntries = function () {
    $.getJSON('/get_num_entries', function(data) {
        console.log('showNumberOfEntries:', data.num_entries);
        $('#num_entries').html(data.num_entries);
        if($("#checkbox").prop("checked")){
            var red = Math.round(getRandomArbitrary(0, 255));
            var green = Math.round(getRandomArbitrary(0, 255));
            var blue = Math.round(getRandomArbitrary(0, 255));
            var color = "rgba(" + red.toString() + ', ' + green.toString() + ', ' + blue.toString() + ', 1';
            $("body").css({color: color});
        }
        else{
            $("body").css({color: 'white'});
        }
    });
};


$(showNumberOfEntries());
$(window.setInterval(showNumberOfEntries, updateInerval));
