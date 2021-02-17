$(function () {
    'use strict';
    var invoice_product, product_name, product_id, product_price, hsn_code;

    function setChart1() {
        var Chart1 = document.getElementById('salesData').getContext('2d');
        var chart = new Chart(Chart1, {
            type: 'line',
            data: {
                labels: ["One", "Two", "Three", "Four", "Five", 'Six', "Seven", "Eight"],
                datasets: [{
                    label: "My First dataset",
                    backgroundColor: 'rgb(255, 99, 132)',
                    borderColor: 'rgb(255, 79, 116)',
                    borderWidth: 2,
                    pointBorderColor: false,
                    data: [5, 10, 5, 8, 20, 30, 20, 10],
                    fill: false,
                    lineTension: .4,
                }, {
                    label: "Month",
                    fill: false,
                    lineTension: .4,
                    startAngle: 2,
                    data: [20, 14, 20, 25, 10, 15, 25, 10],
                    // , '#ff6384', '#4bc0c0', '#ffcd56', '#457ba1'
                    backgroundColor: "transparent",
                    pointBorderColor: "#4bc0c0",
                    borderColor: '#4bc0c0',
                    borderWidth: 2,
                    showLine: true,
                }]
            },

            // Configuration options
            options: {
                title: {
                    display: false
                }
            }
        });
    }

    function setChart2() {
        var chart2 = document.getElementById('salesData1').getContext('2d');
        var myChart = new Chart(chart2, {
            type: 'bar',
            data: {
                labels: ["January", "February", "March", "April", "May", 'Jul'],
                datasets: [{
                    label: "Quantity",
                    fill: false,
                    lineTension: 0,
                    data: [45, 25, 40, 50, 45, 30],
                    pointBorderColor: "#4bc0c0",
                    borderColor: '#4bc0c0',
                    borderWidth: 2,
                    showLine: true,
                }, {
                    label: "Sales",
                    fill: false,
                    lineTension: 0,
                    startAngle: 2,
                    data: [90, 40, 30, 55, 25, 60],
                    // , '#ff6384', '#4bc0c0', '#ffcd56', '#457ba1'
                    backgroundColor: "transparent",
                    pointBorderColor: "#ff6384",
                    borderColor: '#ff6384',
                    borderWidth: 2,
                    showLine: true,
                }],
                options: {
                    scales: {
                        xAxes: [{
                            scaleLabel: {
                                display: true,
                                labelString: 'Sales in months'
                            }
                        }]
                    }
                }
            },
        });
    }
})