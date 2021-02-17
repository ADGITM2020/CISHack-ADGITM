$(function () {

    'use strict';

    // form submit
    $("#invoice-submit").click(function () {
        $("#invoice-form").submit();
    });

    var aside = $('.side-nav'),
        showAsideBtn = $('.show-side-btn'),
        contents = $('#contents'),
        _window = $(window)

    showAsideBtn.on("click", function () {
        $("#" + $(this).data('show')).toggleClass('show-side-nav');
        contents.toggleClass('margin');
    });

    if (_window.width() <= 767) {
        aside.addClass('show-side-nav');
    }

    _window.on('resize', function () {
        if ($(window).width() > 767) {
            aside.removeClass('show-side-nav');
        }
    });

    // dropdown menu in the side nav
    var slideNavDropdown = $('.side-nav-dropdown');

    $('.side-nav .categories li').on('click', function () {

        var $this = $(this)

        $this.toggleClass('opend').siblings().removeClass('opend');

        if ($this.hasClass('opend')) {
            $this.find('.side-nav-dropdown').slideToggle('fast');
            $this.siblings().find('.side-nav-dropdown').slideUp('fast');
        } else {
            $this.find('.side-nav-dropdown').slideUp('fast');
        }
    });

    $('.side-nav .close-aside').on('click', function () {
        $('#' + $(this).data('close')).addClass('show-side-nav');
        contents.removeClass('margin');
    });


    // Start chart
    Chart.defaults.global.animation.duration = 2000; // Animation duration
    Chart.defaults.global.title.display = false; // Remove title
    Chart.defaults.global.title.text = "Chart"; // Title
    Chart.defaults.global.title.position = 'top'; // Title position
    Chart.defaults.global.defaultFontColor = '#999'; // Font color
    Chart.defaults.global.defaultFontSize = 10; // Font size for every label

    // Chart.defaults.global.tooltips.backgroundColor = '#FFF'; // Tooltips background color
    Chart.defaults.global.tooltips.borderColor = 'white'; // Tooltips border color
    Chart.defaults.global.legend.labels.padding = 0;
    Chart.defaults.scale.ticks.beginAtZero = true;
    Chart.defaults.scale.gridLines.zeroLineColor = 'rgba(255, 255, 255, 0.1)';
    Chart.defaults.scale.gridLines.color = 'rgba(255, 255, 255, 0.02)';
    Chart.defaults.global.legend.display = false;

    var invoice_list,price_list,yearSales ,transaction,total_sales,uniqueYears,items_sold;
    $.ajax({
        type: 'GET',
        url: '../api/dashboard/',
        success: function (data) {
            console.log(data);
            invoice_list = data.invoice_list;
            price_list = data.price_list;
            yearSales = data.yearSales;
            uniqueYears = data.year;
            transaction=data.transaction;
            total_sales=data.total_sales;
            items_sold=data.items_sold;
            setChart1();
            setChart3();
            setDetails();
        },
        error: function (error_data) {
            console.log(error_data['responseText'])
        }
    })
    function setDetails() {
        document.getElementById('items_sold').innerText = items_sold;
        document.getElementById('total_sales').innerText = total_sales.toLocaleString('en-IN', {
            maximumFractionDigits: 2,
            style: 'currency',
            currency: 'INR'});
        document.getElementById('transaction-made').innerText = transaction;
    }
    function setChart1() {
        var chart = document.getElementById('myChart');
        var myChart = new Chart(chart, {
            type: 'bar',
            data: {
                labels: invoice_list,
                datasets: [{
                    label: "Sales",
                    fill: false,
                    lineTension: 0,
                    data: price_list,
                    pointBorderColor: "#4bc0c0",
                    borderColor: '#ff6384',
                    borderWidth: 2,
                    showLine: true,
                }
                //     {
                //     label: "Succes",
                //     fill: false,
                //     lineTension: 0,
                //     startAngle: 2,
                //     data: [20000, 40000, 20000, 40050, 25000, 60000],
                //     // , '#ff6384', '#4bc0c0', '#ffcd56', '#457ba1'
                //     backgroundColor: "transparent",
                //     pointBorderColor: "#ff6384",
                //     borderColor: '#ff6384',
                //     borderWidth: 2,
                //     showLine: true,
                // }
                ]
            },
        });
    }

    //  Chart ( 2 )
    var Chart2 = document.getElementById('myChart2').getContext('2d');
    var chart = new Chart(Chart2, {
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
            }, {
                label: "Month",
                fill: false,
                lineTension: .4,
                startAngle: 2,
                data: [40, 20, 5, 10, 30, 15, 15, 10],
                // , '#ff6384', '#4bc0c0', '#ffcd56', '#457ba1'
                backgroundColor: "transparent",
                pointBorderColor: "#ffcd56",
                borderColor: '#ffcd56',
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
    function setChart3() {
        var chart = document.getElementById('chart3');
        var myChart = new Chart(chart, {
            type: 'bar',
            data: {
                labels: uniqueYears,
                datasets: [{
                    label: "Sales",
                    fill: false,
                    lineTension: .3,
                    pointBorderColor: "transparent",
                    pointColor: "white",
                    borderColor: '#4bc0c0',
                    borderWidth: 2,
                    showLine: true,
                    data: yearSales,
                    pointBackgroundColor: 'transparent',
                }]
            },
        });
    }
});