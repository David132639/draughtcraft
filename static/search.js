$(document).ready(function() {
    $( "#search_form" ).submit(function(e) {
        e.preventDefault();
        var search_string = encodeURIComponent($("#search_text").val());
        window.location.replace("/draughtandcraft/search/" + search_string);
    });
});