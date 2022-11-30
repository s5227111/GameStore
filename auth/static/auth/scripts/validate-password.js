const validatePassword = (password) => {
    return password.match(
      /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$/
    );
};

const validateLength = (password) => {
    return password.length >= 8
}

const validateHaveLetters = (password) => {
    return password.match(/(.*[a-z].*)/) && (password.match(/(.*[A-Z].*)/))
}

const validateHaveSpecialChars = (password) => {
    return password.match(/(.*[@$!%*#?&]).*/)
}

const validate_password = () => {

  const $password = $("#inputPassword");
  //const $inputHelp = $('#inputHelp');
  const password = $('#inputPassword').val();
  const $inputHelpLength = $("#inputHelpLength");
  const $inputHelpLetters = $("#inputHelpLetters");
  const $inputHelpSpecialChars = $("#inputHelpSpecialChars");
  const $button = $("#jsDisableButton");
  var valid_len = false;
  var valid_letters = false;
  var valid_chars = false;
    
  // verifica o tamanho da password
  if (validateLength(password)){
    $inputHelpLength.css("color", "#22A861");
    valid_len = true;
    
  } else {
    $inputHelpLength.css("color", "#ea3b52");
    valid_len = false;
  }
  if (validateHaveLetters(password)){
    $inputHelpLetters.css("color", "#22A861");
      valid_letters = true;  
  } else
  {
      $inputHelpLetters.css("color", "#ea3b52");
      valid_letters = false;
    } if (validateHaveSpecialChars(password))
    {
        $inputHelpSpecialChars.css("color", "#22A861")
        valid_chars = true;
    } else
    {
      $inputHelpSpecialChars.css("color", "#ea3b52");
        valid_chars = false;

    // checa se todos os quesitos estão cumpridos
  }if (valid_chars & valid_len & valid_letters)
  {
      $button.removeAttr("disabled", "disabled");
      $password.css("border-color", "#22A861");
      
  } else
  {
      $button.attr("disabled", "disabled");
      $password.css("border-color", "#ea3b52");
      
  }

    
  return false;
    
}

$("#inputPassword").keyup(function(event) {
    validate_password();
});


$('#inputPassword').focusout('input', validate_password); 


