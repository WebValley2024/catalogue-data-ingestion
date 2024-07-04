document.addEventListener('DOMContentLoaded', function() {
    // for every input field, add a class to style it using bootstrap
    var input_fields = document.querySelectorAll('input');
    for (var i = 0; i < input_fields.length; i++) {
        input_fields[i].classList.add('form-control');
    }
    // for every button, add a class to style it using bootstrap
    var buttons = document.querySelectorAll('button');
    for (var i = 0; i < buttons.length; i++) {
        buttons[i].classList.add('btn');
        buttons[i].classList.add('btn-primary');
    }
});