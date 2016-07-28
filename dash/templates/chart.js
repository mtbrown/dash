{% set chart_var = "chart_" + id %}
var {{ chart_var }} = new Chart(document.getElementById("{{ id }}"), {
    type: '{{ chart_type }}',
    data: {
        labels: [{{ labels|map('quote')|join(', ') }}],
        datasets: [{
            {% if description is not none %}label: {{ description|quote }},{% endif %}
            data: [{{ data|map('int')|join(', ') }}],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            xAxes: [{
                type: '{{ x_scale.value }}',
                time: {
                    tooltipFormat: "YYYY-MM-DD hh:mm:ss a"
                }
            }],
            yAxes: [{
                ticks: {
                    {% if max_y is not none %}max: {{ max_y|int }},{% endif %}
                    {% if min_y is not none %}min: {{ min_y|int }},{% endif %}
                }
            }]
        }
    }
});

socket.on('{{ id }}', function(msg) {
    var chart = {{ chart_var }};

    console.log("{{ id }} received " + msg);
    var command = msg[0];
    var data = msg[1];

    if (command == 'add') {
        {% if max_points is defined %}
        if (chart.data.labels.length >= {{ max_points|int }}) {
            chart.data.labels.shift();
            chart.data.datasets[0].data.shift();
        }
        {% endif %}
        chart.data.labels.push(data[0]);
        chart.data.datasets[0].data.push(data[1]);
    }
    else if (command == 'update') {
        chart.data.datasets[0].data[data[0]] = data[1];
    }
    else if (command == 'remove') {
        chart.data.labels.splice(data);
        chart.data.datasets[0].data.splice(data);
    }

    chart.update(0, true);

});