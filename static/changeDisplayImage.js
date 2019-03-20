/*
set the uplaoded image to teh users profile image
displayed at the top of the form
*/
$(document).ready(function(){

	$('#id_image').on('change',function(e){
		if (this.files && this.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#displayImg').attr('src', e.target.result);
            }
            reader.readAsDataURL(this.files[0]);
        }

	});
});