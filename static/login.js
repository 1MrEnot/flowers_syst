const login_tb = $("#login_tb");
const password_tb = $("#password_tb");
const login_button = $("#login_but");


async function login(){
    const login = login_tb.val();
    const password = password_tb.val();
    const data = {
        'login': login,
        'password': password
    }

    $.ajax({
        url: '/login',
        type: 'POST',
        data: JSON.stringify(data),
        contentType:"application/json; charset=utf-8",
        dataType: 'json',
        success: (data, textStatus) => {
            if (data.redirect) {
                window.location.href = data.redirect;
            }
        },
        error: (jqXHR) => {
            alert(jqXHR.responseJSON.error);
        }
    });
}

login_button.on('click', login);
