function get_chart(x, y) {
    const labels = x;

    const ctx = document.getElementById('myChart');
    var mychart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {

                    label: 'Titulo',
                    data: y,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.5)',
                        'rgba(255, 159, 64, 0.5)',
                        'rgba(255, 205, 86, 0.5)',
                        'rgba(75, 192, 192, 0.5)',
                        'rgba(54, 162, 235, 0.5)',
                        'rgba(153, 102, 255, 0.5)',
                        'rgba(201, 203, 207, 0.5)'
                    ],
                    borderColor: [
                        'rgb(255, 99, 132)',
                        'rgb(255, 159, 64)',
                        'rgb(255, 205, 86)',
                        'rgb(75, 192, 192)',
                        'rgb(54, 162, 235)',
                        'rgb(153, 102, 255)',
                        'rgb(201, 203, 207)'
                    ],

                    borderWidth: 1,
                },
                // {
                //     label: 'Fevereiro',
                //     data: [12, 15],
                //     backgroundColor: [

                //         'rgba(255, 159, 64, 0.2)',

                //     ],
                //     borderColor: [

                //         'rgb(255, 159, 64)',

                //     ],

                //     borderWidth: 1,
                // }
            ]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    return mychart;
}