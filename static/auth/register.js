
// 회원가입
async function loginregister() {
    $('.error').text("")
    let formData = new FormData();
    let userid = $("#RegisterUserId ").val();
    let username = $("#RegisterUserName ").val();
    let userpw = $("#RegisterUserPw ").val();
    let userpw2 = $("#RegisterUserPwChek").val();
    if (!checkUserId(userid)) {
        return false;
    }
    if (!await useridchek(userid)){ 
        return false;
    }
    if (!checkName(username)){
        return false;
    }
    if (!checkPassword(userid, userpw, userpw2)){
        return false;
    }  
    formData.append("userid", userid);
    formData.append("userpw", userpw);
    formData.append("username", username);
    fetch("/auth/register", { method: "POST", body: formData }).then((res) => res.json()).then((data) => { 
        if(data["result"] == "success"){
            Swal.fire({
                icon: 'success',            
                title: '가입 완료!',         
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.reload();
                }
            });                  
        }else{
            Swal.fire({
                icon: 'error',             
                title: '가입 실패',         
            });
        }
    });
}
//공백 확인 함수
function checkExistData(value) {
    if (value == "" || value == null) {
        //alert(dataName + " 입력해주세요!");
        return false;
    }
    return true;
}
// 아이디 유효성
function checkUserId(id) {
    var idRegExp = /^[a-zA-z0-9]{4,12}$/; //아이디 유효성 검사
    //Id가 입력되었는지 확인하기
    if (!checkExistData(id)){
        $('#idError').text('아이디를 입력해 주세요.');
        return false;
    }else if (!idRegExp.test(id)) {
        $('#idError').text('영문 대소문자와 숫자 4~12자리로 입력해야합니다!');
        $("#RegisterUserId ").val("");
        return false;
    }else{
        $('#idError').text('');
    }
    return true; //확인이 완료되었을 때
}
// 이름 유효성
function checkName(name) {
    var nameRegExp = /^[가-힣]{2,7}$/;
    if (!checkExistData(name)){
        $('#nameError').text('이름을 입력해 주세요.');
        return false; 
    }else if (!nameRegExp.test(name)) {
        $('#nameError').text('이름이 올바르지 않습니다.');
        return false;
    }else{
        $('#nameError').text('');
    }
    return true; //확인이 완료되었을 때
}
//비밀번호 검사
function checkPassword(id, password1, password2) {
    var password1RegExp = /^[a-zA-z0-9]{4,12}$/; //비밀번호 유효성 검사
    //비밀번호가 입력되었는지 확인하기
    if (!checkExistData(password1)){
        $('#pwError').text('비밀번호를 입력해 주세요.');
        return false;            
    }else if (!password1RegExp.test(password1)) {
        $('#pwError').text('영문 대소문자와 숫자 4~12자리로 입력해야합니다!');
        $("#RegisterUserPw ").val("");
        return false;
    }else {
        $('#pwError').text('');
    }
    if (!checkExistData(password2)){ //비밀번호 확인이 입력되었는지 확인하기
        $('#pwCheckError').text('비밀번호확인를 입력해 주세요.');
        return false;           
    }else if (password1 != password2) { //비밀번호와 비밀번호 확인이 맞지 않다면..
        $('#pwCheckError').text('두 비밀번호가 맞지 않습니다.');
        $("#RegisterUserPw ").val("");
        $("#RegisterUserPwChek").val("");
        return false;
    }else if (id == password1) { //아이디와 비밀번호가 같을 때..
        $('#pwCheckError').text('아이디와 비밀번호는 같을 수 없습니다!');
        $("#RegisterUserPw ").val("");
        $("#RegisterUserPwChek").val("");
        return false;
    }else{
        $('#pwCheckError').text('');
    }
    return true; //확인이 완료되었을 때
}
// 아이디중복확인
async function useridchek(userid) {
    let formData = new FormData();  
    formData.append("userid", userid);

    var idcheck = await fetch('/auth/useridcheck',{ method: "POST", body: formData });
    var data = await idcheck.json();
    console.log(data['result'])
    if(data['result'] == true){
        $('#idError').text('사용가능한 아이디 입니다.');
        $('#idError').css("color","green");                                
        return true;
    }else{
        $('#idError').text('사용중인 아이디 입니다.');
        $('#idError').css("color","red");  
        return false;
    }
}
// 회원 탈퇴
function deleteUser() {
    fetch("/auth/delete")
        .then((res) => res.json())
        .then((data) => {
            alert(data['msg'])
            location.href = "/"
        });
}