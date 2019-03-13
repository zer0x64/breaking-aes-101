$( document ).ready(() => {
    $("#btn_get_token").click(() => {
        $.ajax('api/encrypt', {
            data: JSON.stringify({'username': $("#name_input").val()}),
            contentType: "application/json",
            type: "POST",
            success: (data) => {
                $("#token_box").text(data)
            }
        })
    })

    $("#btn_verify").click(() => {
        $.ajax('api/verify', {
            data: JSON.stringify({'token': $("#token_input").val()}),
            contentType: "application/json",
            type: "POST",
            success: (data) => {
                $("#verify_box").text(data)
            }
        })
    })
})
