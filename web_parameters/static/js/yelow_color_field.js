yellow_color = function () {
            console.log('123123213');
            var massege = $("div#flash_massage").text().split(' ');
            var len = massege.length;
            console.log(massege);
            var input_field = massege[len - 1];
            console.log(input_field);
            console.log("input[name='" + input_field + "']")
            $("input[name=" + input_field + "]").css("background-color", "yellow");
};

$(document).ready(yellow_color());