//helper function to set the parameters of teh google map
function displayMap(long,lats) {
  var coords = {lat: lats, lng: long};
  var map = new google.maps.Map(
      document.getElementById('map'), {zoom: 15, center: coords});
  var marker = new google.maps.Marker({position: coords, map: map});
}

//callback for  async defer
//only initialised if the business lat and long exists
function initMap(){
	var paramReq = new XMLHttpRequest();
	var pubName = document.getElementById("map").getAttribute('data-name')
	paramReq.onreadystatechange = function(){

		//get the the lat and long of the business
		if(paramReq.readyState==4 && paramReq.status==200){
			var response = JSON.parse(paramReq.responseText)
			displayMap(response["lng"],response["lat"])
		}
	}

	paramReq.open("GET","/draughtandcraft/api/mapApi/"+pubName)
	paramReq.send()




}