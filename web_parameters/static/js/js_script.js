updateInerval = 1 * 1000;  // ms

showNumberOfEntries = function () {
    console.log('showNumberOfEntries');
    $.getJSON('/show_entries', function(data) {
            $('#num_entries').html(data.num_entries);
        }
    });
}

$(showNumberOfEntries());
$(window.setInterval(showNumberOfEntries, updateInerval));
