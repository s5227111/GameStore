// TABLE OF CONTENTS
// 1.0 - Validate email functions
// 2.0 - Validate Username functions
// 3.0 - Validate Password functions
// 4.0 - Confirm Password functions
// 5.0 - Call validation functions


// Validate email filed
// Note: email input filed is email-type. The browser will validate this field for us.
// Also, we will check if the email is already in use using backend validation.
// We just need to check if the email is filled.
// 1.0 - Validate email functions

const validate_email = () => {

    $email = $("#email");
    $submit = $("#submit");

    // check if email matches regex
    if (!($email.val().match(/^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/)))
    {
        // If email is not valid, disable the submit button and show error message
        $submit.attr("disabled", "disabled");
        return false;
    }
    return true;

}


// Validate Username filed
// Note: For our purpose, we will consider a valid username a string with at least 5 characters, just being letters and numbers.
// Also, we will check if the username is already in use using backend validation.
// 2.0 - Validate Username functions

const validate_username = () => {
    
    const $username = $("#username");
    const $submit = $("#submit");
    const $usernameHelp = $('#usernameHelp');

    // Match username with regex
    if (!($username.val().match(/^[a-zA-Z0-9]{5,}$/)))
    {
        // if username is not valid, disable the submit button and show error message
        $usernameHelp.text("The username must have at least 5 characters, just being letters and numbers.")
        $submit.attr("disabled", "disabled");
        return false
    } 
    // Either, returns true and erase the error message
    $usernameHelp.text("")
    return true
}

// Validate Password filed
// Note: For our purpose, we will consider a valid password a string with at least 8 characters, containing at least one letter, one number and one special character.
// 3.0 - Validate Password functions

// check if password has at least 8 characters

const validateLength = (password) => {
    return password.length >= 8
}

// check if password has at least one letter and one number
const validateHaveLetters = (password) => {
    return password.match(/(.*[a-z].*)/) || (password.match(/(.*[A-Z].*)/))
}

// check if password has at least one special character
const validateHaveSpecialChars = (password) => {
    return password.match(/(.*[@$!%*#?&]).*/)
}

// check if password is valid
const validate_password = () => {

    const $password = $("#password");
    const $passwordLength = $("#passwordLength");
    const $passwordLetters = $("#passwordLetters");
    const $passwordSpecialChars = $("#passwordSpecialChars");
    const $submit = $("#submit");
    const password = $('#password').val();
    
    // flag to check if password is valid
    var lengthValid = false;
    var specialCharsValid = false;
    var lettersValid = false;


    // If password contains at least 8 characters, ```validateLength``` will be in green color, otherwise, it will be in gray color and the submit button will be disabled
    if (validateLength(password))
    {   
        $passwordLength.css("color", "green");
        lengthValid = true;
        
    } else
    {
        $submit.attr("disabled", "disabled");
        $passwordLength.css("color", "#6c757d");
        lengthValid = false;
    }
    // If password contains at least one letter and one number, ```validateHaveLetters``` will be in green color, otherwise, it will be in gray color and the submit button will be disabled
    if (validateHaveLetters(password))
    {
        $passwordLetters.css("color", "green");
        lettersValid = true;
    }
    else
    {
        $submit.attr("disabled", "disabled");
        $passwordLetters.css("color", "#6c757d");
        lettersValid = false;
    }
    // If password contains at least one special character, ```validateHaveSpecialChars``` will be in green color, otherwise, it will be in gray color and the submit button will be disabled
    if (validateHaveSpecialChars(password))
    {
        $passwordSpecialChars.css("color", "green");
        specialCharsValid = true;
    }
    else
    {
        $submit.attr("disabled", "disabled");
        $passwordSpecialChars.css("color", "#6c757d");
        specialCharsValid = false;
    }

    // if password is not valid, disable the submit button
    if (!lengthValid || !lettersValid || !specialCharsValid)
    {
        return false;
    }else{
        return true;
    }
}

// Confirm Password filed
// Functions to check if the password and the confirm password are the same
// 4.0 - Confirm Password functions

const validate_confirm_password = () => {

    // if passwords match, then enable the submit button
    if (($("#password").val() === $("#confirmPassword").val()) && ($("#password").val() !== ""))
    {
        $("#confirmPasswordHelp").text("")
        return true;

    // Either, disable the submit button, and display an error message
    } else{

        $("#submit").attr("disabled", "disabled");
        $("#confirmPasswordHelp").text("Passwords do not match.")
        return false;
    }
}


// 5.0 - Enable submit button if all fields are valid

const enable_submit = () => {
    if (validate_email() && validate_username() && validate_password() && validate_confirm_password())
    {
        $("#submit").removeAttr("disabled");
    }else{
        $("#submit").attr("disabled", "disabled");
 
    }
}

// 6.0 Call validation functions
// Keyup events

$("#email").keyup(function (event) {
    validate_email();
    enable_submit();
});
$("#username").keyup(function (event) {
    validate_username();
    enable_submit();

});

$("#password").keyup(function(event) {
    validate_password();
    enable_submit();
});

$("#confirmPassword").keyup(function (event) {
    validate_confirm_password();
    enable_submit();
});


// Focusout events
$('#email').focusout('input', validate_email);
$('#password').focusout('input', validate_password); 
$('#username').focusout('input', validate_username);
$('#confirmPassword').focusout('input', validate_confirm_password);



