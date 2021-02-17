
$('#vehicle-btn').click(function (e) {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: 'create/',
        data: {
            vehicle_driver: $('#veh_driver').val(),
            vehicle_no: $('#veh_no').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function () {
            alert("created successfully")
        }
    })
});

$('#generate-files').click(function (e) {
    e.preventDefault();
    $.ajax({
        type: 'GET',
        url: 'generate/',
        success: function () {
            $('#view-pdf-without-link').removeClass('hidden')
            $('#download-pdf').removeClass('hidden')
            $('#download-excel').removeClass('hidden')
            $('#generate-files').addClass('hidden')
        }
    })
});

$('#view-pdf-without-link').click(function (e) {
    e.preventDefault();
    $.ajax({
        type: 'GET',
        url: 'convertpdf/',
        data: {
            'bill_no':$('#bill-no').textContent,
            'year':$('#invoice-year').textContent
        },
        success: function (data) {
            $(this).attr("href", data)
            window.open(data,'_blank')
            location.href = location.href
        },
        error:function (e) {
            console.log(e.responseText)
        }
    })
});

$('#add_more').click(function () {
    var form_idx = $('#id_form-TOTAL_FORMS').val();
    $('#product-form').append($('#empty_form').html().replace(/__prefix__/g, form_idx));
    form_idx.val(parseInt(form_idx) + 1);
});

$(".btn-circle-download").click(function() {
  $(this).addClass("load");
  setTimeout(function() {
    $(".btn-circle-download").addClass("done");
  }, 1000);
  setTimeout(function() {
    $(".btn-circle-download").removeClass("load done");
  }, 5000);
});
