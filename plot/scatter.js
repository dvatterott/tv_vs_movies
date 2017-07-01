// http://bl.ocks.org/peterssonjonas/4a0e7cb8d23231243e0e

var margin = { top: 100, right: 300, bottom: 50, left: 50 },
    outerWidth = 1050,
    outerHeight = 500,
    width = outerWidth - margin.left - margin.right,
    height = outerHeight - margin.top - margin.bottom;

var parseTime = d3.time.format("%Y-%m-%d").parse;

var xCat = "first_air_date",
    yCat = "vote_average",
    rCat = "popularity",
    title = "show_name";

d3.csv("shows.csv", function(data) {
  data.forEach(function(d) {
    d.first_air_date = parseTime(d.first_air_date);
    d.vote_average = +d.vote_average;
    d.popularity = +d.popularity;
    d.show_name = d.show_name;
    d.vote_count = +d.vote_count;
  });

  // define the x scale (horizontal)
  var mindate = new Date(1950,0,1),
      maxdate = new Date(2017,0,31);

  var y = d3.scale.linear().range([height, 0]).nice().domain([3, 9]);
  var x = d3.time.scale()
      .domain([mindate, maxdate])    // values between for month of january
      .range([0, width - 0 * 2]);   // map these the the chart width = total

  var yMax = d3.max(data, function(d) { return d[yCat]; }),
      yMin = d3.min(data, function(d) { return d[yCat]; }),
      yMin = yMin > 0 ? 0 : yMin;

  var xAxis = d3.svg.axis()
      .scale(x)
      .orient("bottom")
      .tickSize(-height)
      .tickFormat(d3.time.format("%Y"));

  var yAxis = d3.svg.axis()
      .scale(y)
      .orient("left")
      .tickSize(-width);

  var color = d3.scale.category10();

  var tip = d3.tip()
      .attr("class", "d3-tip")
      .offset([-10, 0])
      .html(function(d) {
        return "Show Title: " + d['show_name'] + "<br>" + "Rating: " + d[yCat];
      });

  var zoomBeh = d3.behavior.zoom()
      .x(x)
      .y(y)
      .scaleExtent([1, 5])
      .on("zoom", zoom);

  var svg = d3.select("#scatter")
    .append("svg")
      .attr("width", outerWidth)
      .attr("height", outerHeight)
    .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
      .call(zoomBeh);

  svg.call(tip);

  svg.append("rect")
      .attr("width", width)
      .attr("height", height);

  svg.append("g")
      .classed("x axis", true)
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)
    .append("text")
      .classed("label", true)
      .attr("x", width*.5+margin.left)
      .attr("y", margin.bottom - 10)
      .style("text-anchor", "end")
      .text(xCat);

  svg.append("g")
      .classed("y axis", true)
      .call(yAxis)
    .append("text")
      .classed("label", true)
      .attr("transform", "rotate(-90)")
      .attr("x", 0-(height/2)+margin.bottom)
      .attr("y", -margin.left)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text(yCat);

  var objects = svg.append("svg")
      .classed("objects", true)
      .attr("width", width)
      .attr("height", height);

  objects.append("svg:line")
      .classed("axisLine hAxisLine", true)
      .attr("x1", 0)
      .attr("y1", 0)
      .attr("x2", width)
      .attr("y2", 0)
      .attr("transform", "translate(0," + height + ")");

  objects.append("svg:line")
      .classed("axisLine vAxisLine", true)
      .attr("x1", 0)
      .attr("y1", 0)
      .attr("x2", 0)
      .attr("y2", height);

  objects.selectAll(".dot")
      .data(data)
    .enter().append("circle")
    .filter(function(d) { return d.vote_count > 10 })
      .classed("dot", true)
      .attr("r", function (d) { return 6 * Math.sqrt(d[rCat] / Math.PI); })
      .attr("transform", transform)
      .style("fill", function(d) { return color(0); })
      .on("mouseover", tip.show)
      .on("mouseout", tip.hide);

  function zoom() {
    svg.select(".x.axis").call(xAxis);
    svg.select(".y.axis").call(yAxis);

    svg.selectAll(".dot")
        .attr("transform", transform);
  }

  function transform(d) {
    return "translate(" + x(d[xCat]) + "," + y(d[yCat]) + ")";
  }
});
