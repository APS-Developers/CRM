const ctx = document.getElementById('piechart').getContext('2d');
fetch("/slainfo").then((res) => res.json()).then((res) => {
    createPieChart(res);
}).catch((err) => {
    alert(err);
})
fetch("/slainfomonthly").then((res) => res.json()).then((res) => {
    createBarChart(res);
}).catch((err) => {
    alert(err);
})

function createPieChart(data) {
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
}

function createBarChart(data){
    
    var ctx2 = document.getElementById('linechart').getContext('2d');
    var myChart2 = new Chart(ctx2, {
        type: 'line',
        data: {
            labels: data.months,
            datasets: [

                {
                    type: 'line',
                    label: 'Total',
                    data: data.total,
                    backgroundColor: '#F40090',
                    borderColor: '#F40090',

                    borderWidth: 1
                },
                {
                    type: 'bar',
                    label: 'Within SLA',
                    data: data.within,
                    backgroundColor: [
                        '#F0A07C',

                    ],

                    borderWidth: 1
                },
                {
                    type: 'bar',
                    label: 'Outside SLA',
                    data: data.outside,
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