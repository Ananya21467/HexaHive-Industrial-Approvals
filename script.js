document.querySelector("button").onclick = () =>{
    //success prompt
    alert("logoin successful");

    const emailInput = document.querySelector("input[type='email']").value;
     const passwordInput = document.querySelector("input[type='password']").value;

     if(emailInput.trim() === "" || passwordInput.trim( )=== ""){
        alert("Please enter both your collge email and password to proceed. ");
        return;
     }

    window.location.href = "landing.html";
};
