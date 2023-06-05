// 로그인 알림창 (Swal)
const Toast = Swal.mixin({
    toast: true,
    position: 'center-center',
    showConfirmButton: false,
    timer: 1000,
    timerProgressBar: true,
    didOpen: (toast) => {
    toast.addEventListener('mouseenter', Swal.stopTimer)
    toast.addEventListener('mouseleave', Swal.resumeTimer)
    }
})
//로그인
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
                Toast.fire({
                    icon: 'success',
                    title: data["msg"]
                }).then(function(){
                    location.href = "/board/list";
                });               
            } else {
                Toast.fire({
                    icon: 'error',
                    title: data["msg"]
                }).then(function(){
                    location.reload();
                });
            }
        });
    
}
// 로그아웃
function userLogout() {
    
    fetch("/auth/logout")
        .then((res) => res.json())
        .then((data) => {
            let isLogout = data['result']

            if (isLogout) {
                Toast.fire({
                    icon: 'success',
                    title: data["msg"]
                }).then(function(){
                    location.href = "/"
                });  
            } else {
                Toast.fire({
                    icon: 'success',
                    title: data["msg"]
                }).then(function(){
                    location.reload();
                });  
            }
        });
}


