socket.on('{{ id }}', function(msg) {
    console.log("{{ id }} received " + msg);
    $('#{{ id }}').prepend(msg);
});