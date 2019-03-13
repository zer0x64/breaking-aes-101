$.get('api/leak', (data) => {
    $("#secret_ciphertext").text(data)
})

$( document ).ready(() => {
    $("#btn_decrypt").click(() => {
        $.ajax('api/decrypt', {
            data: JSON.stringify({'data': $("#decrypt_input").val()}),
            contentType: "application/json",
            type: "POST",
            success: (data) => {
                $("#decrypt_box").text(data)
            },
            error: (error) => {
                if(error.status == 500) {
                    $('#decrypt_box').text("Internal server error! The server probably couldn't decrypt or decode the data.")
                }
            }
            
        })
    })

    $("#btn_verify").click(() => {
        $.ajax('api/verify', {
            data: JSON.stringify({'key': $("#key_input").val()}),
            contentType: "application/json",
            type: "POST",
            success: (data) => {
                $("#verify_box").text(data)
            }
        })
    })
})
