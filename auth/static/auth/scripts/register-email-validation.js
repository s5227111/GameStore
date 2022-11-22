const validateEmail = (email) => {
    return email.match(
      /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    );
};
const validate_email = () => {


  const $email = $("#inputEmail");
  const $inputHelp = $('#inputHelp');
  const email = $('#inputEmail').val();
  const $button = $("#jsDisableButton");
  
  if (validateEmail(email)) {
      $email.css("border-color", "green");
    $inputHelp.text("")
    $button.removeAttr('disabled');
    
  } else {
      $email.css("border-color", "red");
    $inputHelp.text("Utilize o formato nome@exemplo.com.")
    $button.attr("disabled", "disabled");
  }
  return false;
    
}

$("#inputEmail").keyup(function(event) {
  //var current_pass = $(this).val();
  
  validate_email();

});

$('#inputEmail').focusout('input', validate_email); 


// show modal
const modal = document.getElementById("modalMessage");
const $errorMessage = $("#errorMessage");

if ($errorMessage.attr("data-value") === "True")
{
  modal.showModal();
}


