function useAPI() {
    var url = "https://www.boredapi.com/api/activity"
	console.log("making fetch to", url)
	fetch(url)
		.then(resp=>{return resp.json()})
		.then(json=>{
			console.log(json.text)
			document.getElementById("activityRand").innerHTML = json.activity
		})

}
function useAPIRec() {
    var url = "http://www.boredapi.com/api/activity?type=recreational"
	console.log("making fetch to", url)
	fetch(url)
		.then(resp=>{return resp.json()})
		.then(json=>{
			console.log(json.text)
			document.getElementById("activityRec").innerHTML = json.activity
		})

}


document.addEventListener("DOMContentLoaded", () => {
  console.log("Hello World!");
});