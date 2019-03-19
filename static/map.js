






function displayMap(long,lats) {
  // The location of Uluru
  var coords = {lat: lats, lng: long};
  // The map, centered at Uluru
  var map = new google.maps.Map(
      document.getElementById('map'), {zoom: 4, center: coords});
  // The marker, positioned at Uluru
  var marker = new google.maps.Marker({position: coords, map: map});
}


function initMap(){

	var paramReq = new XMLHttpRequest();
	var pubName = document.getElementById("map").getAttribute('data-name')
	paramReq.onreadystatechange = function(){

		if(paramReq.readyState==4 && paramReq.status==200){
			var response = JSON.parse(paramReq.responseText)
			alert(response["lng"])
			alert(response["lat"])
			displayMap(response["lng"],response["lat"])
		}
	}

	paramReq.open("GET","/draughtandcraft/api/mapApi/"+pubName)
	paramReq.send()




}