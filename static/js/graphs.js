let yieldData = {chartID:"yield-chart", label:"Yield - Gb", data:yields}
let clusterDensityData = {chartID:"clusterDensity-chart", label:"Clusters - K/mm2", data:clusterDensity}
let passFilterData = {chartID:"passFilter-chart", label:"Pass Filter - %", data:passFilter}
let q30Data = {chartID:"q30-chart", label:"q30 Score - %", data:q30}
let chemistryData = {chartID:"chemistry-chart", labels:["High300", "Mid300", "Mid150"], data: chemistries}
let experimentData = {chartID:"experiment-chart", labels:["Genome", "Exome", "Capture"], data: experiments}


function getResponsiveStyles() {
    let responsiveStyles = {};
    let xs = window.matchMedia("(min-width: 1px) and (max-width: 575px)");
    let sm = window.matchMedia("(min-width: 576px) and (max-width: 767px)");
    let md = window.matchMedia("(min-width: 768px) and (max-width: 991px)");
    let lg = window.matchMedia("(min-width: 992px)");

    if(xs.matches) {
        responsiveStyles.xAxisFontSize = 12;
        responsiveStyles.yAxisFontSize = 10;
        responsiveStyles.padding = 0;
        console.log(responsiveStyles.axisFontSize);
    } else if(sm.matches) {
        responsiveStyles.xAxisFontSize = 14;
        responsiveStyles.yAxisFontSize = 12;
        responsiveStyles.padding = 10;
        console.log(responsiveStyles.axisFontSize);
    } else if(md.matches) {
        responsiveStyles.xAxisFontSize = 16;
        responsiveStyles.yAxisFontSize = 16;
        responsiveStyles.padding = 15;
        console.log(responsiveStyles.axisFontSize);
    } else if(lg.matches) {
        responsiveStyles.xAxisFontSize = 18;
        responsiveStyles.yAxisFontSize = 18;
        responsiveStyles.padding = 20;
        console.log(responsiveStyles.axisFontSize);
    }
    return responsiveStyles;
}


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
                    fontSize: responsiveStyles.xAxisFontSize,
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
                    fontSize: responsiveStyles.yAxisFontSize,
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

function getPieChart(chartData) {
    new Chart(document.getElementById(chartData.chartID), {
        type: 'pie',
        data: {
        labels: chartData.labels,
        datasets: [{
            backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f"],
            data: chartData.data
        }]
        },
        options: {
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
            responsive: true,
            maintainAspectRatio: false
        }
    });
}

/**
 * Function is called on resize event and reloads page so responsive styles are added to charts. sizeTimeout and clearTimeout are used to prevent firing of multiple resize events. 
 */
let resizeTimeout;
window.addEventListener('resize', function() {
  clearTimeout(resizeTimeout);
  resizeTimeout = setTimeout(function(){
    window.location.reload();
  }, 1500);
});

/**
 * get line and pie charts when page is fully loaded
 */
document.addEventListener("DOMContentLoaded", function() {
    getLineChart(yieldData);
    getLineChart(clusterDensityData);
    getLineChart(passFilterData);
    getLineChart(q30Data);
    getPieChart(chemistryData);
    getPieChart(experimentData);
});
