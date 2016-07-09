var ctx = document.getElementById("{{ id }}");
var chart = new Chart(ctx, {
    type: '{{ chart_type }}',
    data: {
        labels: [{{ labels|map('quote')|join(', ') }}],
        datasets: [{
            label: '# of Votes',
            data: [],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        }
    }
});

socket.on('{{ id }}', function(msg) {
    console.log("{{ id }} received " + msg);
    var command = msg[0];
    var data = msg[1];

    if (command == 'add') {
        chart.data.labels.push(data[0]);
        chart.data.datasets[0].data.push(data[1]);
    }

    chart.update();

});