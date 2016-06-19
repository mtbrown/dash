socket.on('{{ id }}', function(msg) {
    console.log("{{ id }} received " + msg);
    document.getElementById('{{ id }}').textContent=msg;
});