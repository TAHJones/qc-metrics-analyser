var lineChartOptions = {
    legend: {
        display: false,
        position: 'top',
        labels: {
        boxWidth: 40,
        fontColor: "#3776b3",
        fontSize: 20
        }
    },
    scales: {
        xAxes: [{
        gridLines: {
            display: false
        },
        scaleLabel: {
            display: true,
            labelString: "Pool Number",
            padding: 10,
            fontColor:  "#3776b3",
            fontSize: 18,
            fontStyle: "italic"

        }
        }],
        yAxes: [{
        gridLines: {
            color: "#3776b3",
            borderDash: [5, 10],
        },
        scaleLabel: {
            display: true,
            labelString: "Yield - Gigabases",
            padding: 10,
            fontColor:  "#3776b3",
            fontSize: 18,
            fontStyle: "italic"
        }
        }]
    },
    layout: {
        padding: {
            left: 0,
            right: 0,
            top: 30,
            bottom: 10
        }
    },
    maintainAspectRatio: false
};

var pieChartOptions = {
    legend: {
        display: true,
        position: "right"
    },
    layout: {
        padding: {
            left: 0,
            right: 0,
            top: 0,
            bottom: 10
        }
    },
    maintainAspectRatio: false
};

new Chart(document.getElementById("yield-chart"),{
    "type":"line",
    "data":
        {"labels":labels, 
        "datasets":[{"label":"Yield - Gigabases",
        "data":	yields, 
        "fill":false,
        "borderColor":"rgb(75, 192, 192)",
        "lineTension":0.1}]},
    "options": lineChartOptions
});

new Chart(document.getElementById("clusterDensity-chart"),{
    "type":"line",
    "data":
        {"labels":labels, 
        "datasets":[{"label":"Cluster Density - K/mm2",
        "data":	clusterDensity, 
        "fill":false,
        "borderColor":"rgb(75, 192, 192)",
        "lineTension":0.1}]},
    "options": lineChartOptions
});

new Chart(document.getElementById("passFilter-chart"),{
    "type":"line",
    "data":
        {"labels":labels, 
        "datasets":[{"label":"Clusters Pass Filter - %",
        "data":	passFilter, 
        "fill":false,
        "borderColor":"rgb(75, 192, 192)",
        "lineTension":0.1}]},
    "options": lineChartOptions
});

new Chart(document.getElementById("q30-chart"),{
    "type":"line",
    "data":
        {"labels":labels, 
        "datasets":[{"label":"q30 - %",
        "data":	q30, 
        "fill":false,
        "borderColor":"rgb(75, 192, 192)",
        "lineTension":0.1}]},
    "options": lineChartOptions
});

new Chart(document.getElementById("chemistry-chart"), {
    type: 'pie',
    data: {
    labels: ["High300", "Mid300", "Mid150"],
    datasets: [{
        label: "Sequencing Chemistries",
        backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f"],
        data: chemistries
    }]
    },
    options: pieChartOptions
});

new Chart(document.getElementById("experiment-chart"), {
    type: 'pie',
    data: {
    labels: ["Genome", "Exome", "Capture"],
    datasets: [{
        label: "Sequencing Experiments",
        backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f"],
        data: experiments
    }]
    },
    options: pieChartOptions
});