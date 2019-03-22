
$(document).ready(function() {
      function split( val ) {
        //helper function to get the most recent item in text box
      return val.split( /,\s*/ );
    }
    function extractLast( term ) {
      //gets the most recent item in the textbox
      return split( term ).pop();
    }
 
    $("#form_auto")
      //dont change focus on tab
      .on( "keydown", function( event ) {
        if ( event.keyCode === $.ui.keyCode.TAB &&
            $( this ).autocomplete( "instance" ).menu.active ) {
          event.preventDefault();
        }
      })
      .autocomplete({
        //query api with recent item to get matches
        source: function( request, response ) {
          $.getJSON( "/draughtandcraft/api/"+$('#form_auto').data("context"), {
            term: extractLast( request.term )
          }, response );
        },
        search: function() {
          // custom minLength
          var term = extractLast( this.value );
          if ( term.length < 2 ) {
            return false;
          }
        },
        focus: function() {
          // prevent value inserted on focus
          return false;
        },
        select: function( event, ui ) {
          //add the selected item replacing the current text
          //after the last comma
          var terms = split( this.value );
          terms.pop();
          terms.push( ui.item.value );
          terms.push( "" );
          this.value = terms.join( ", " );
          return false;
        }
      });
});

