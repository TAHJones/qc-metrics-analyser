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

function getResponsiveStyles() {
    let responsiveStyles = {};
    let xs = window.matchMedia("(min-width: 1px) and (max-width: 575px)");
    let sm = window.matchMedia("(min-width: 576px) and (max-width: 767px)");
    let md = window.matchMedia("(min-width: 768px) and (max-width: 991px)");
    let lg = window.matchMedia("(min-width: 992px)");

    if(xs.matches) {
        responsiveStyles.axisFontSize = 12;
        responsiveStyles.padding = 0;
        console.log(responsiveStyles.axisFontSize);
    } else if(sm.matches) {
        responsiveStyles.axisFontSize = 14;
        responsiveStyles.padding = 10;
        console.log(responsiveStyles.axisFontSize);
    } else if(md.matches) {
        responsiveStyles.axisFontSize = 16;
        responsiveStyles.padding = 15;
        console.log(responsiveStyles.axisFontSize);
    } else if(lg.matches) {
        responsiveStyles.axisFontSize = 18;
        responsiveStyles.padding = 20;
        console.log(responsiveStyles.axisFontSize);
    }
    return responsiveStyles;
}


let yieldData = {chartID:"yield-chart", label:"Yield - Gigabases", data:yields}
let clusterDensityData = {chartID:"clusterDensity-chart", label:"Cluster Density - K/mm2", data:clusterDensity}
let passFilterData = {chartID:"passFilter-chart", label:"Clusters Pass Filter - %", data:passFilter}
let q30Data = {chartID:"q30-chart", label:"q30 - %", data:q30}

function getLineChart(chartData) {
    let responsiveStyles = getResponsiveStyles();
    new Chart(document.getElementById(chartData.chartID),{
        "type":"line",
        "data":
            {"labels":labels, 
            "datasets":[{"label":chartData.label,
            "data":	chartData.data, 
            "fill":false,
            "borderColor":"rgb(75, 192, 192)",
            "lineTension":0.1}]},
        "options": {
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
                    padding: 5,
                    fontColor:  "#3776b3",
                    fontSize: responsiveStyles.axisFontSize,
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
                    labelString: chartData.label,
                    padding: 10,
                    fontColor:  "#3776b3",
                    fontSize: responsiveStyles.axisFontSize,
                    fontStyle: "italic"
                }
                }]
            },
            layout: {
                padding: {
                    left: responsiveStyles.padding,
                    right: responsiveStyles.padding,
                    top: responsiveStyles.padding,
                    bottom: responsiveStyles.padding
                }
            },
            responsive: true,
            maintainAspectRatio: false
        }
    });
}

getLineChart(yieldData);
getLineChart(clusterDensityData);
getLineChart(passFilterData);
getLineChart(q30Data);


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