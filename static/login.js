const login_button = $(".log_but");
const reg_click = $(".reg");

function reg_write() {
    var result = document.getElementById("log_reg");
    result.innerHTML = "";

    result.innerHTML = `
    <p class="log">Регистрация</p>
        <p class="data_user">Имя:</p>
        <input type="text" id="name_input">
        <p class="data_user">Логин:</p>
        <input type="text" id="login_input">
        <p class="data_user">Пароль:</p>
        <input type="password" id="pass_input">
        <p class="data_user">Повторите пароль:</p>
        <input type="password" id="pass_rep_input">
        <p class="log_r">Вход</p>
        <input class="log_but" type="button" value="Зарегистрироваться">
        `;

    const log_click = $(".log_r");
    log_click.on('click', log_write);
    $(".log_but").on('click', register);
}

function log_write() {
    var result = document.getElementById("log_reg");
    result.innerHTML = "";

    result.innerHTML = `
        <p class="log">Вход</p>
        <p class="data_user">Логин:</p>
        <input type="text" id="login_tb">
        <p class="data_user">Пароль:</p>
        <input type="password" id="password_tb">
        <p class="reg">Регистрация</p>
        <input class="log_but" type="button" value="Войти">`;

    const reg_click = $(".reg");
    reg_click.on('click', reg_write);
}

function login(){
    const login = $("#login_tb").val();
    const password = $("#password_tb").val();
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

function register(){
    const name = $("#name_input").val();
    const email = $("#login_input").val();
    const pass = $("#pass_input").val();
    const pass_repeat = $("#pass_rep_input").val();

    if (!(name || email || pass || pass_repeat)){
        return alert("Введите все поля!");
    }

    if (pass != pass_repeat){
        return alert("Пароли не совпадают!");
    }

    const reg_obj = {
        name: name,
        email: email,
        password: pass
    };

    fetch('/api/user', {
      method: 'POST',
      headers: {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(reg_obj)
    })
    .then(res => {
        if (res.ok){
            alert("Вы успешно зарегестрировались!")
        }
        else{
            alert("Не удалось зарегесрироваться");
        }
    });

}

login_button.on('click', login);
reg_click.on('click', reg_write);
