var height = window.innerHeight;
var width = window.innerWidth;

/* Initial Line graph Overview */

var svgH = height * 0.7, svgW = 'fit-content'

var svg = d3.select('#overview').append("svg")
    .attr('id', 'line-overview')
    .attr('width', svgW)
    .attr('height', svgH);

var fullCount; // The entire frequency by date dataset

var lineFunc = d3.line()
    .x(function(d){ return d.Count })
    .y(function(d){ return svgH -d.Frequency * 20 });

var cleanCounter = 0;

var lineFuncClean = d3.line()
    .x(function(d, i){
        let xValue;
        if (fullCount[i].Frequency == 0){
            xValue = fullCount[cleanCounter].Count;
        } else{
            xValue = d.Count;
        }
        return xValue * 0.8
    })
    .y(function(d, i){
        let yValue
        if (d.Frequency == 0){
            yValue = fullCount[cleanCounter].Frequency;
        } else {
            yValue = d.Frequency;
            cleanCounter = i;
        }
        return svgH-yValue * 20;
    })

d3.csv("../tweets-count.csv", function(d){
    fullCount = d; // returns the entire dataset in d3v4 

    svg.append('path')
        .attr('d', lineFuncClean(fullCount))
        .attr('stroke', '#000')
        .attr('fill', 'none');
});
