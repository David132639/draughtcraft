$(document).ready(function(){
    var stock_url = window.location.protocol + "//" + window.location.host + window.location.pathname
    stock_url += "stock"

    var is_in_stock = null;

    function updateStockInfo() {
        $.get( stock_url).done(
            function() {
                console.log("we hit beer stocked");
                $("#change_stock_status").html("Remove beer from stock list.");
                is_in_stock = true;
            }
        )
        .fail(
            function() {
                console.log("we hit beer not stocked");
                $("#change_stock_status").html("Add beer to stock list.");
                is_in_stock = false;
            }
        );
    }

    $("#change_stock_status").click(
        function(e) {
            e.preventDefault();

            if(is_in_stock) {
                $.ajax(
                    {
                        url: stock_url,
                        type: "DELETE",
                        success: function() {
                            location.reload();
                        }
                    }
                );
            } else {
                $.ajax(
                    {
                        url: stock_url,
                        type: "POST",
                        success: function() {
                            location.reload();
                        }
                    }
                );
            }
        }
    );

    updateStockInfo();
});