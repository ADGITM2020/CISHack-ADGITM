$(document).ready(function () {
    var jobCount = $('#product-table-body .product-row').length;
    $('.list-count').text(jobCount + ' items');


    $("#search-text").keyup(function () {

        var searchTerm = $("#search-text").val();
        var searchSplit = searchTerm.replace(/ /g, "'):containsi('")

        //extends :contains to be case insensitive
        $.extend($.expr[':'], {
            'containsi': function (elem, i, match, array) {
                return (elem.textContent || elem.innerText || '').toLowerCase()
                    .indexOf((match[3] || "").toLowerCase()) >= 0;
            }
        });


        $("#product-table-body .product-title").not(":containsi('" + searchSplit + "')").each(function (e) {
            $(this).parent().parent().addClass('hiding out').removeClass('product-row');
            console.log("not contaisn"+$(this).parent("tr").length);
            setTimeout(function () {
                $('.out').addClass('hidden');
            }, 300);
        });

        $("#product-table-body .product-title:containsi('" + searchSplit + "')").each(function (e) {
            $(this).parent().parent().removeClass('hidden out').addClass('product-row');
            setTimeout(function () {
                $('.product-row').removeClass('hiding');
            }, 1);
        });


        var jobCount = $('#product-table-body .product-row').length;

        //shows empty state text when no jobs found
        if (jobCount === '0') {
            $('#product-table-body').addClass('empty');
        } else {
            $('#product-table-body').removeClass('empty');
        }

    });


    function searchList() {
        //array of list items
        var listArray = [];

        $("#product-table-body .product-title").each(function () {
            var listText = $(this).text().trim();
            listArray.push(listText);
        });

        $('#search-text').autocomplete({
            source: listArray
        });


    }

    searchList();

});







