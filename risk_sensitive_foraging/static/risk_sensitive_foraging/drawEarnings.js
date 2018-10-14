function drawEarnings(target, s, b, mls, maxx, showx, showb, xLabel) {
  var bLabel = b.toString();
  var bLabelIndent = b < 10 ? -6 : -12;

  $(function () {
    Highcharts.chart(target, {
      chart: {
        events: {
          load: function() {
            start = window.performance.now();
          }
        },
        type: 'bar',
        margin: [0, 3, 25, 15], /*20, 50, 25, 124*/
      },
      xAxis: { /*This is actually the y-axis of the barchart */
        visible: false
      },
      yAxis: { /* That is the x axis*/
        visible: showb,
        title: { text: null },
        labels: { enabled: true },
        width: maxx * 20,
        min: -.001,
        max: maxx - .10,
        lineColor: 'grey',        
        lineWidth: 1,
        startOnTick: false,
        gridLineWidth: 0,
        tickInterval: 1,
        tickWidth: 1,
        tickLength: 5,
        tickPositions: [0, s, b, maxx],
        minorTicks: true,
        tickColor: 'grey',
        minorTickInterval: 1,
        minorTickLength: 5,
        minorTickColor: 'grey',    
        /* line and label for the goal*/
        plotLines: [{
          color: 'rgb(97,169,176)',
          value: b - .025,
          width: 2,
          zIndex: 4}]
      },
      plotOptions: {
        series: {
          visible: showx,
          stacking: 'normal',
          dataLabels: { enabled: false },
          animation: {
            duration: 500
          }
        },
        area: {
          dataLabels: {
            enabled: true,
            crop: false,
            overflow: 'none'
          }
        },
      },
      series: [{
        data: [ s ],
        color: s < b ? 'rgb(207,216,220)' : 'rgb(141, 230, 230)',
        borderColor: s < b ? 'rgb(207,216,220)' : 'rgb(141, 230, 230)',
        borderWidth: 2,
        minPointLength: 1
      }]
    });
  });
}
