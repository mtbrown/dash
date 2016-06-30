socket.on('{{ id }}', function(msg) {
    console.log("{{ id }} received " + msg);
    $("#{{ id }}").text(msg);
});