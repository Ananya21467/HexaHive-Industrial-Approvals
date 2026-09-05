document.querySelector("button").onclick = () =>{
    //success prompt
    alert("login successful");

    const emailInput = document.querySelector("input[type='email']").value;
     const passwordInput = document.querySelector("input[type='password']").value;

     if(emailInput.trim() === "" || passwordInput.trim( )=== ""){
        alert("Please enter both your email and password to proceed. ");
        return;
     } 

     const lowerEmail = emailInput.toLowerCase().trim();

    
    if (lowerEmail.includes("admin") || lowerEmail.includes("gov") || lowerEmail.includes("authority")) {
        // If it's an admin/authority email, bypass the hub and go straight to your dashboard!
        alert("Welcome Back, Authority Officer.");
        window.location.href = "authority-dashboard.html";
    } else {
        // Otherwise, send standard applicants to your central landing hub menu
        alert("Login successful!");
        window.location.href = "landing.html";
    }

     
window.location.href = "landing.html";
   
};
