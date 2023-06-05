function userLogin() {

    // form 태그 데이터를 받아옴
    let loginFormData = new FormData();
    let userid = $("input[name='userid']").val();
    let userpw = $("input[name='userpw']").val();

    loginFormData.append('userid', userid)
    loginFormData.append('userpw', userpw)

    // id 확인
    fetch("/auth/login", { method: "POST", body: loginFormData })
        .then((res) => res.json())
        .then((data) => {
            let isLogin = data['result']
            
            if (isLogin) {
                alert(data['msg'])
                location.href = "/board/list"
            } else {
                alert(data['msg'])
                location.reload();
            }
        });
    
}

function userLogout() {
    
    fetch("/auth/logout")
        .then((res) => res.json())
        .then((data) => {
            let isLogout = data['result']

            if (isLogout) {
                alert(data['msg'])
                location.href = "/"
            } else {
                alert(data['msg'])
                location.reload();
            }
        });
}


