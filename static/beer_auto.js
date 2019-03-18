
$(document).ready(function() {
  $("#beer_auto").autocomplete({
    source: "/draughtandcraft/api/get_beers/",
    minLength: 2,
  });
});