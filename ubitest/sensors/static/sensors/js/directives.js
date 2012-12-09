'use strict';

/* Directives */
angular.module('ubiApp.directives', []).
  directive('appVersion', ['version', function(version) {
    return function(scope, elm, attrs) {
      elm.text(version);
    };
  }]).
  directive('jvVisualization',[function(){
    
    var m = [10,10,100,40],
    m2 = [430,10,20,40],
    cwidth = 920,
    cheight = 500,
    width = cwidth-m[1]-m[3],
    height = cheight-m[0]-m[2],
    height2 = cheight - m2[0] - m2[2],
    color = d3.interpolateRgb("#f77", "#77f");

    var numlines = 2;


    return{
      restrict:'A',
      link:function(scope,elements,attrs){
        //Crear SVG Inicial
        var values =[];
        for(var i=0; i<numlines;i++){
            var ln = []
            for(var j=0; j<10;j++){
              ln.push( {date: new Date(2012,0,1,j,0), value:Math.random()*10
              }); 

            }
          values.push(ln)
        }

        //#Generador de lineas
        var line = d3.svg.line()
          .x(function(d) { return x(d.date); })
          .y(function(d) { return y(d.value); });

        var nav_line = d3.svg.line()
          .x(function(d) { return x2(d.date); })
          .y(function(d) { return y2(d.value); });


        
        //#Eje X superior
        console.log(width);
        var x = d3.time.scale().range([0,width]);
        var xAxis = d3.svg.axis().scale(x).tickSubdivide(true);
        x.domain([values[0][0].date, values[0][values[0].length - 1].date]);
        
        //#Eje X inferior
        var x2 = d3.time.scale().range([0,width]);
        var xAxis2 = d3.svg.axis().scale(x2).tickSubdivide(true);
        x2.domain([values[0][0].date, values[0][values[0].length - 1].date]);
        
        //#Eje Y superior
        var y = d3.scale.linear().range([height, 0]),
        yAxis = d3.svg.axis().scale(y).ticks(4).orient("left");
        y.domain([0,10]);
        //#Eje Y Inferior
        var y2 = d3.scale.linear().range([height2, 0]),
        yAxis2 = d3.svg.axis().scale(y2).ticks(4).orient("left");
        y2.domain([0,10]);

        //#Definicon del Evento Brush
        var brush = d3.svg.brush()
            .x(x2)
            .on("brush", brush);


        //#Append del SVG inicial
        var graphic = d3.select(elements[0])
          .append("svg")
            .attr("width", width+m[1]+m[3])
            .attr("height",height+m[0]+m[2])
   

        //#Group para el panel principal
        var principal = graphic.append("g")
            .attr("transform", "translate(" + m[3] + "," + m[0] + ")")
            .attr("class","principal")
            .attr("width",width)
            .attr("height",height)

        //#Group para el panel de navegacion
        var nav = graphic.append('g')
            .attr("transform","translate("+ m2[3] +"," + m2[0] + ")");

        //#Eje x panel principal
        principal.append("svg:g")
          .attr("class", "x axis")
          .attr("transform", "translate(0," + height + ")")
          .call(xAxis);

        //#Eje x panel navegacion
        nav.append("svg:g")
          .attr("class", "x axis")
          .attr("transform", "translate(0," + height2 + ")")
          .call(xAxis2);

        //#Eje y panel principal
        principal.append("svg:g")
            .attr("class", "y axis")
            .call(yAxis);


        //#Agregar un Layer por cada grafica
        var layers = principal.selectAll('.layers')
          .data(values)
          .enter()
          .append("g")
          .attr("class","layers")


        //#Agregar la linea correspondiente a cada layer
        layers.append("svg:path")
          .attr("class", "line")
          .attr("clip-path", "url(#clip)")
          .attr("d", function(d){return line(d)});



        //#Agregar un Layer por cada grafica a navegacion
        var nav_layers = nav.selectAll('.layers')
          .data(values)
          .enter()
          .append("g")
          .attr("class","layers")


        //#Agregar la linea correspondiente a cada layer
        nav_layers.append("svg:path")
          .attr("class", "line")
          .attr("clip-path", "url(#clip)")
          .attr("d", function(d){return nav_line(d)});

        //
        nav.append("g")
            .attr("class", "x brush")
            .call(brush)
          .selectAll("rect")
            .attr("y", -6)
            .attr("height", height2 + 7);


        //#Funcion de brush
        function brush(){
          x.domain(brush.empty() ? x2.domain() : brush.extent());
          layers.selectAll("path").attr("d", function(d){return line(d)});
          principal.select(".x.axis").call(xAxis);
        }

      }
    }
  }]);