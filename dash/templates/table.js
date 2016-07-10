socket.on('{{ id }}', function(msg) {
    console.log("{{ id }} received " + msg);
    var max_rows = {{ max_rows|int }};

    // delete last row if max_rows reached
    if (max_rows > 0 && $('#{{ id }} tr').length >= max_rows) {
        $('#{{ id}} tr:last').remove();
    }

    var html = "<tr>"
    for (var i = 0; i < msg.length; i++) {
        html += "<td>" + msg[i] + "</td>"
    }
    html += "</tr>"

    $('#{{ id }}').prepend(html);
});