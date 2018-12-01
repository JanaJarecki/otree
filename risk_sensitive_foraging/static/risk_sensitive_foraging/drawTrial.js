  function drawTrial(target, show, trial, ntrials, tLabel) {
    ntrials = Array(ntrials).fill(1);
    bg_col_future = 'transparent';
    bg_col_current = bg_col_future; //'rgb(207,216,220)';
    bg_col_past = 'rgba(56,56,56,.05)';
    txt_col_past = 'rgba(56,56,56,.3)';
    txt_col_current = 'black';
    txt_col_future = 'rgba(56,56,56,.8)';

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
            y: -18,
            formatter(self) {
              trial = this.chart.series[1].options.data.length;
              var v = this.value + 1;
              if (v < trial) {
                  return '<span style="fill: ' +txt_col_past +' ;">' + v + '</span>';
              } else if (v == trial) {
                  return '<span style="fill: ' +txt_col_current +'; font-weight: bold; text-decoration: underline; ">' + v + '</span>';
              } else {
                return '<span style="fill: ' +txt_col_future +' ;">' + v + '</span>';
               }
              },
            style: {
              'color': txt_col_future,
              'fontSize': '16px'
            }            
          }
        },
        yAxis: { visible: false },
        plotOptions: {
          scatter: {
            marker: {
              radius: 13,
              lineWidth: 1.5,
              lineColor: bg_col_past,
              symbol: 'circle',
            }
          },
          series: { visible: show }
        },
        series: [{
            color: bg_col_future,
            data: ntrials,
          },
          {
            data: Array(trial).fill(1),
            color: bg_col_current,
            zoneAxis: 'x',
              zones: [{
                value: trial-1,
                color: bg_col_past
              }]
          }],
        });
    });
}

