var ctx = document.getElementById("{{ id }}");
var myChart = new Chart(ctx, {
    type: '{{ chart_type }}',
    data: {
        labels: [{{ labels|map('quote')|join(', ') }}],
        datasets: [{
            label: '# of Votes',
            data: [12, 19, 3, 5, 2, 3],
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