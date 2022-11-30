const validateUsername = (username) => {
    return username.match(
      /^[a-zA-Z0-9_]{4,}[a-zA-Z]+[0-9]*$/
    );
};
const validate_username = () => {

  const $username = $("#inputUsername");
  const $inputHelp = $('#inputHelp');
  const username = $('#inputUsername').val();
  const $button = $("#jsDisableButton");
  
  if (validateUsername(username)) {
    $username.css("border-color", "green");
    $inputHelp.text("")
    $button.removeAttr('disabled');
    
  } else {
    $username.css("border-color", "red");
    $inputHelp.text("O nome de usuário deve conter no mínimo 5 caracteres, sendo apenas letras ou números")
    $button.attr("disabled", "disabled");
  }
  return false;
    
}

$("#inputUsername").keyup(function(event) {
  //var current_pass = $(this).val();
  
  validate_username();

});

$('#inputUsername').focusout('input', validate_username); 


// show modal
const modal = document.getElementById("modalMessage");
const $errorMessage = $("#errorMessage");

if ($errorMessage.attr("data-value") === "True")
{
  modal.showModal();
}


