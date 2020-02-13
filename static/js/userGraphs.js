new Chart(document.getElementById("yield-chart"),{
    "type":"line",
    "data":
        {"labels":labels, 
        "datasets":[{"label":"Yield - Gigabases",
        "data":	yields, 
        "fill":false,
        "borderColor":"rgb(75, 192, 192)",
        "lineTension":0.1}]},
    "options":{}});

new Chart(document.getElementById("clusterDensity-chart"),{
    "type":"line",
    "data":
        {"labels":labels, 
        "datasets":[{"label":"Cluster Density - K/mm2",
        "data":	clusterDensity, 
        "fill":false,
        "borderColor":"rgb(75, 192, 192)",
        "lineTension":0.1}]},
    "options":{}});

new Chart(document.getElementById("passFilter-chart"),{
    "type":"line",
    "data":
        {"labels":labels, 
        "datasets":[{"label":"Clusters Pass Filter - %",
        "data":	passFilter, 
        "fill":false,
        "borderColor":"rgb(75, 192, 192)",
        "lineTension":0.1}]},
    "options":{}});

new Chart(document.getElementById("q30-chart"),{
    "type":"line",
    "data":
        {"labels":labels, 
        "datasets":[{"label":"q30 - %",
        "data":	q30, 
        "fill":false,
        "borderColor":"rgb(75, 192, 192)",
        "lineTension":0.1}]},
    "options":{}});

    new Chart(document.getElementById("chemistry-chart"), {
        type: 'pie',
        data: {
        labels: ["Genome", "Exome", "Capture"],
        datasets: [{
            label: "Sequencing Chemistries",
            backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f"],
            data: chemistries
        }]
        },
        options: {
            title: {
                display: true,
                text: 'Sequencing Chemistries'
            }
        }
    });

    new Chart(document.getElementById("experiment-chart"), {
        type: 'pie',
        data: {
        labels: ["High300", "Mid300", "Mid150"],
        datasets: [{
            label: "Sequencing Experiments",
            backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f"],
            data: experiments
        }]
        },
        options: {
            title: {
                display: true,
                text: 'Sequencing Experiments'
            }
        }
    });