function getOptionFormValues(option) {

}

function saveAjaxOptionAForm(event) {

}

function readyFn( jQuery ) {
    console.log( "ready!" );
    $('#optionA').find('button').click({'option':'#optionA'}, saveAjaxOptionAForm);
    $('#optionB').find('button').click({'option':'#optionB'}, saveAjaxOptionAForm);
}

$( document ).ready(readyFn);