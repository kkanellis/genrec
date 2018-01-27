
// Initialize Pie Chart
// ----------------------------------------------------------------------------
color_map = {
  blues: '#3B3EAC',
  classical: '#00BFFF',
  country: '#FF9900',
  disco: '#990099',
  hiphop: '#808080',
  jazz: '#8B4513',
  metal: '#000000',
  pop: '#DD4477',
  reggae: '#109618',
  rock: '#8B0707',
}

const CHART = document.getElementById("chart");
Chart.defaults.global.animation.duration = 1000;

let labels = ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock'];

let backgroundColors = [ ];
let initialData = [ ];

for (let i = 0; i < labels.length; i++) {
  let color = color_map[ labels[i] ];
  color = Color(color).alpha(0.7).rgbString();
  backgroundColors.push(color);

  initialData.push( 0 );
}

barChart = new Chart(CHART, {
  type: 'pie',
  data: {
    labels: labels,
    datasets: [{
      label: "Confidence",
      backgroundColor: backgroundColors,
      data: initialData,
    }]
  },
  options: {
    layout: {
      padding: 15,
    },
    legend: {
      display: true,
      position: 'left',
    },
  }
});


// Randomize data for testing
// ----------------------------------------------------------------------------
function RandomizeChartData (chart, interval) {
  this.chart = chart;
  this.interval = interval;

  this.start = function() {
    this.intervalID = setInterval(function() {
      chart.data.datasets.forEach( (dataset) => {
        for (i = 0; i < dataset.data.length; i++) {
          dataset.data[i] = Math.random();
        }
      });
      chart.update(); 
    }, this.interval);
  }

  this.stop = function() {
    clearInterval(this.intervalID);
  }
}

function UpdateChartData (chart, ytplayer, predictions, checkInterval) {
    this.chart = chart;
    this.ytplayer = ytplayer;
    this.predictions = jQuery.extend(true, {}, predictions);
    this.checkInterval = checkInterval;

    this.start = function() {
        this.intervalID = setInterval(function() {
            elapsedSeconds = ytplayer.getCurrentTime().toFixed(0);
            chart.data.datasets.forEach( (dataset) => {
                if (predictions[elapsedSeconds] != null) {
                    for (i = 0; i < 10; i++) {
                        dataset.data[i] = predictions[elapsedSeconds][i];
                    }
                }
            });
            chart.update();
        }, this.checkInterval);
    }

    this.stop = function() {
        clearInterval(this.intervalID);
    }
}

//var randData = new RandomizeChartData(barChart, 1000);
//randData.start();
// ----------------------------------------------------------------------------

/*document.getElementById('shuffle').addEventListener('click', function() {
  barChart.update();
});*/

