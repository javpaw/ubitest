'use strict';

/* Directives */
angular.module('ubiApp.directives', []).
  directive('appVersion', ['version', function(version) {
    return function(scope, elm, attrs) {
      elm.text(version);
    };
  }]).
  directive('jvVisualization',[function(){
    
    var m = [80,80,80,80],
    cwidth = 960,
    cheight = 500,
    width = cwidth-m[1]-m[3],
    height = cheight-m[0]-m[2],
    color = d3.interpolateRgb("#f77", "#77f");

    var numlines = 2;


    return{
      restrict:'A',
      link:function(scope,elements,attrs){
        //Crear SVG Inicial
        
        var graphic = d3.select(elements[0])
          .append("svg")
            .attr("width", width+m[1]+m[3])
            .attr("height",height+m[0]+m[2])
          .append("svg:g")
            .attr("transform", "translate(" + m[3] + "," + m[0] + ")");

        var x = d3.time.scale().range([0,width]);
        var xAxis = d3.svg.axis().scale(x).tickSubdivide(true);

        var values =[];
        for(var i=0; i<numlines;i++){
            line = []
            for(var j=0; j<10;j++){
              line.push( {date: new Date(2012,0,1,j,0), value:Math.random()*10
              }); 

            }
          values.push(line)
        }
        x.domain([values[0][0].date, values[0][values[0].length - 1].date]);

          // Add the x-axis.
        graphic.append("svg:g")
          .attr("class", "x axis")
          .attr("transform", "translate(0," + height + ")")
          .call(xAxis);

         var y = d3.scale.linear().range([height, 0]),
            yAxis = d3.svg.axis().scale(y).ticks(4).orient("left");

        y.domain([0,10]);

        // Add the y-axis.
        graphic.append("svg:g")
            .attr("class", "y axis")
            .attr("transform", "translate(" + 0 + ",0)")
            .call(yAxis);

        // A line generator, for the dark stroke.
        var line = d3.svg.line()
            .interpolate("monotone")
            .x(function(d) { return x(d.date); })
            .y(function(d) { return y(d.value); });

        var sensor = graphic.selectAll('.sensor')
          .data(values)
          .enter()
          .append("g")
          .attr("class","sensor")
           
        // Add the line path.
        var pth = sensor.append("svg:path")
            .attr("class", "line")
            .attr("clip-path", "url(#clip)")
            .attr("d", function(d){return line(d)});

        sensor.selectAll("circle")
          .data(function(d){return d})
          .enter()
          .append("circle")
          .attr("class","circ")
          .attr("r",3.5)
          .attr("cx",function(d){return x(d.date)})
          .attr("cy",function(d){return y(d.value)})
          .style("fill","red")


      }
    }
  }]);