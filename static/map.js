
function displayMap(long,lats) {
  var coords = {lat: lats, lng: long};
  var map = new google.maps.Map(
      document.getElementById('map'), {zoom: 15, center: coords});
  var marker = new google.maps.Marker({position: coords, map: map});
}


function initMap(){

	var paramReq = new XMLHttpRequest();
	var pubName = document.getElementById("map").getAttribute('data-name')
	paramReq.onreadystatechange = function(){

		if(paramReq.readyState==4 && paramReq.status==200){
			var response = JSON.parse(paramReq.responseText)
			displayMap(response["lng"],response["lat"])
		}
	}

	paramReq.open("GET","/draughtandcraft/api/mapApi/"+pubName)
	paramReq.send()




}