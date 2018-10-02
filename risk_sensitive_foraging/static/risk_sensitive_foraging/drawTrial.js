  function drawTrial(target, show, trial, ntrials, tLabel) {
    ntrials = Array(ntrials).fill(1);

    $(function () {
      Highcharts.chart(target, {
        chart: {
          type: 'scatter',
          margin: [0, 0, 2, 0]
        },
        xAxis: {
          visible: show,
          min: -.5,
          max: ntrials.length - 0.5,
          lineColor: 'transparent',
          tickLength: 0,
          tickInterval: 1,
          labels: {
            y: -20,
            formatter() { return this.value + 1 },
            style: {
              color: 'black',
            }            
          }
        },
        yAxis: { visible: false },
        plotOptions: {
          scatter: {
            marker: {
              radius: 11,
              lineWidth: 0,
              lineColor: 'black',
              symbol: 'circle',
            }
          },
          series: { visible: show }
        },
        series: [{
            color: 'transparent',
            data: ntrials,
          },
          {
            data: Array(trial).fill(1),
            color: 'rgb(207,216,220)',
            zoneAxis: 'x',
              zones: [{
                value: trial-1,
                color: 'rgba(56,56,56,.5)'
              }]
          }],
        });
    });
}

