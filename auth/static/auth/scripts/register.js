const validateEmail = (email) => {
    return email.match(
      /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    );
};
  
const validateUsernameLength = (username) => {
  if (username.length < 5)
  {
    return false
  } else
  {
    return true
  }
}
const validate_email = () => {


  const $email = $("#email");
  const $result = $('#result');
  const email = $('#email').val();
  $result.text('');
  
  if (validateEmail(email)) {
    $email.css("border-color", "green");
    
  } else {
    $email.css("border-color", "red");
  }
  return false;
    
}
  
const validate_username = () => {
  
  const $username_error = $("#username-error");
  const $username = $("#username");
  const username = $("#username").val();

  if (validateUsernameLength(username))
  {
    $username.css("border-color", "green");
    $username_error.text("");
  } else
  {
    $username.css("border-color", "red");
    $username_error.text("Username inválido! O username deve ter entre 6 e 10 caracteres contendo apenas letras");
  }

// Validations
$('#email').focusout('input', validate_email); 
$("#username").focusout("input", validate_username);
$("#username").focusout("input", validateUserNameAviability);
                          