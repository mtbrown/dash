socket.on('{{ id }}', function(msg) {
    console.log("{{ id }} received " + msg);

    var html = "<tr>"
    for (var i = 0; i < msg.length; i++) {
        html += "<td>" + msg[i] + "</td>"
    }
    html += "</tr>"

    $('#{{ id }}').prepend(html);
});