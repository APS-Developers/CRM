const ctx = document.getElementById('piechart').getContext('2d');
fetch("/slainfo").then((res) => res.json()).then((res) => {
    createCharts(res);
}).catch((err) => {
    alert(err);
})

function createCharts(data) {
    const myChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Within SLA', 'Outside SLA '],
            datasets: [{
                label: 'SLA Status',
                data: [data.within,data.outside],
                backgroundColor: [
                    '#800020',
                    '#de818e',

                ],
                hoverOffset: 6
            }]
        },
        options: {
            responsive: true
        }
    });

    var ctx2 = document.getElementById('linechart').getContext('2d');
    var myChart2 = new Chart(ctx2, {
        type: 'line',
        data: {
            labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
            datasets: [

                {
                    type: 'line',
                    label: 'Total',
                    data: [19, 11, 14, 12, 21, 31],
                    backgroundColor: '#F40090',
                    borderColor: '#F40090',

                    borderWidth: 1
                },
                {
                    type: 'bar',
                    label: 'Within SLA',
                    data: [12, 19, 3, 5, 2, 3],
                    backgroundColor: [
                        '#F0A07C',

                    ],

                    borderWidth: 1
                },
                {
                    type: 'bar',
                    label: 'Outside SLA',
                    data: [18, 1, 13, 10, 2, 13],
                    backgroundColor: [
                        '#4A274F',

                    ],

                    borderWidth: 1
                }

            ]
        },
        options: {
            responsive: true
        }
    });
}