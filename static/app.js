const labels = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
];

const data = {
    datasets: [{
        label: 'Влажность',
        backgroundColor: 'rgb(255, 99, 132)',
        borderColor: 'rgb(255, 99, 132)',
        data: [
            {x:'06-11-2016', y:20},
            {x:'07-11-2016', y:10},
            {x:'08-11-2016', y:12},
        ],
        tension: 0.3
    }]
};

const config = {
    type: 'line',
    data: data,
    options: {}
};

const canvas = document.getElementById('myChart');
const myChart = new Chart(canvas, config);