<center><h1>Auth</h1></center>
<p>This module contains important tools for routes involving user tables and their respective interactions. In this document I list the main obligations and responsibilities present in this package, as well as the current business model
</p>
<hr>
<section>
    <h2>Table of contents</h2>
    <ul>
        <li>Mapped routes</li>
        <li> User model</li>
        <li> What our tests cover?</li>
        <li> Not yet implemented </li>
    </ul>
</section>
<hr>
<section>
    <h2>Mapped Routes</h2>
    <ul>
        <li>
            <h3>Login Page</h3>
            <small>auth.login</small>
            <p>
            This route is responsible for authenticating an already registered user. At its core is the external <em>``flask-login``</em> plugin, which is responsible for adding special methods like the <em>``@login_required``</em> and <em>``current_user``</em> decorators.  This allows you to get the information of the user in the current section (logged in or not) and change the behavior of the pages reactively.
            For more details about how these methods are implemented, you will see more details in the section about the user model, especially about the class <em>``UserMixin``</em>.
            </p>
            <h4>Client-Side and Server-side Validations<h4>
            <p>
            Due to the simplicity of this route, complex client-side validation is not required. In fact, it is only done by checking that all fields in the login form have been filled in (using the ``required`` flag in the input).
When submitting the registration form, a request of type ``POST`` is made to this same endpoint. In this case, it is checked to see if the credentials are correct. If so, the user is redirected to the ``profile-page`` endpoint. Otherwise, the page is rendered and the variable ``wrong_credentials`` is passed to the front-end, allowing a warning message to be displayed  
            </p>
        </li>
        <li>
            <h3>Register Page</h3>
            <small>auth.register</small>
            <h4>Client-Side and Server-Side Validations</h4>
            <p>
            Unlike ``auth.login``, this route needs a script written in javascript to perform the data validations. All this validation is done by the static ``auth.js`` file, present in ``auth/scripts/auth.js`` (relative to auth.static). To ensure consistency of data, this validation is performed in the following steps:
            </p>
        </li>
    <ul>
</section>

#TODO 
