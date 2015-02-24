var data1 = [4, 8, 15, 16, 23, 42];

var jsonData = {};

var results = [0,0,0,0,0,0,0,0,0,0,0,0,0];

$.getJSON("/AcademyAwards.json", function(data){
	console.log(data);

	jsonData = data;
	useData();
});

function useData(){
	$.each(jsonData, function(year, data){
		var rDate = new Date(data['ReleaseDate'] * 1000)
		var aDate = new Date(data['AwardDate'] * 1000)
		var diff = Math.ceil((aDate - rDate)/1000/60/60/24/7/4);
		var movie = data['Movie']
		if(diff > 0 && diff < 13){
			results[diff]++;
		}
	});

	drawChart();
}

function drawChart(){

	console.log(results);

	var x = d3.scale.linear()
	    .domain([0, d3.max(results)])
	    .range([0, 420]);

	d3.select("body .chart")
	  .selectAll("div")
	    .data(results)
	  .enter().append("div")
	    .style("width", function(d) { return x(d) + "px"; })
	    .text(function(d) { return d; });
}
