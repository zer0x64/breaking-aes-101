$.get('api/leaks', (data) => {
    ciphertexts = $("#secret_ciphertext")
    $.each(data, (_, d) => {
        $("<li/>").text(d).appendTo(ciphertexts)
    })
})

$( document ).ready(() => {
    $("#btn_verify").click(() => {
        $.ajax('api/verify', {
            data: JSON.stringify({'data': $("#flag_input").val()}),
            contentType: "application/json",
            type: "POST",
            success: (data) => {
                $("#verify_box").text(data)
            }
        })
    })
})
