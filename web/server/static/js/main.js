// Global
var ytplayer = null;
var barChart = null;
var chartUpdater = null;

// UI
hideElement('preferences-section');
hideElement('chart-section');

// Websockets communication
// -----------------------------------------------------------------------------
var connection = new WebSocket("ws://localhost:8080/ws")

// When the connection is open, send some data to the server
// connection.onopen = function () {
//  var youtube_link = 'https://www.youtube.com/watch?v=nppKPgdc_u0';
//};

function sendValidationUrlMessage (url) {
  var validate_url = {
    "command" : "VALIDATE_URL_REQ",
    "url" : url,
  };

  connection.send(JSON.stringify(validate_url)); // Send the message to the server
};

function sendUserPreferencesMessage (dataset, classifier) {
// Construct an object to test if server knows when to predict a song
  var user_preferences = {
    "command" : "PREDICT_REQ",
    "dataset" : dataset,
    "classifier": classifier,
    "videoId" : videoId,
  };

  connection.send(JSON.stringify(user_preferences)); // Send the message to the server
}

// Log errors
connection.onerror = function (error) {
  console.log('WebSocket Error ' + error);
};

// Log messages from the server
connection.onmessage = function (e) {
  reply = JSON.parse(e.data)
  console.log(reply);

  if (!reply.success) {
    console.error('Server: ' + reply.message);
  }
  else {
    console.info('Server: ' + reply.message);
  }
  
  // Handle received message
  if (reply.command == 'VALIDATE_URL_REP') {
    handleValidationUrlSuccess(reply);
  }
  else if (reply.command == 'PREDICT_REP') {
    handlePredictionSuccess(reply);
  }
  else {
    console.error('Invalid command received: ' + reply.command);
  }
};

// -----------------------------------------------------------------------------

// Youtube link
// -----------------------------------------------------------------------------

var videoId = "";

$('#btn-yt-url').click(function () {
    url = document.getElementById("input-yt-url").value;
    processVideo(url);
});

/* Checks if the provided url belongs to a youtube video */
function matchYoutubeUrl(url) {
    var p = /^(?:https?:\/\/)?(?:m\.|www\.)?(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))((\w|-){11})(?:\S+)?$/;
    if (url.match(p)){
        return url.match(p)[1];
    }
    return null;
}

function processVideo(url) {
    // UI
    setButtonStatus('btn-yt-url', 'Processing...');
    
    videoId = matchYoutubeUrl(url);
    if (!videoId) {
        showErrorModal("Invalid link! Please enter a valid YouTube video url.");
        unsetButtonStatus('btn-yt-url', 'Process');
        return;
    }

    // and that the video is not very long (maybe 5 minutes limit?)
    NProgress.start();
    sendValidationUrlMessage(url);

    // Simulate req-rep
    //setTimeout(function() {
    //    unsetButtonStatus('btn-yt-url', 'Process');
    //}, 20000);
}

function handleValidationUrlSuccess(reply) {
    NProgress.done();
    unsetButtonStatus('btn-yt-url', 'Process');

    if (!reply.success) {
        showErrorModal("Invalid link! Please enter a valid YouTube video url.");
        return;
    }

    showElement('preferences-section');
    windowScrollTo('preferences-section');
}

// -----------------------------------------------------------------------------
var chartUpdater = null;

$('#btn-preferences').click(function (e) {
    
    e.preventDefault();
    NProgress.start();
    setButtonStatus('btn-preferences', 'Saving...');

    clf_name = $('input[name="radio-classifier"]:checked').val();

    sendUserPreferencesMessage('gtzan', clf_name);
    
    setButtonStatus('btn-preferences', 'Working...');
});

function handlePredictionSuccess(reply) {
    unsetButtonStatus('btn-preferences', 'Save Preferences');
    console.log(reply);

    // Change overall prediction text
    document.getElementById('overall-prediction-text').innerHTML =
        "Our classifier, trained on the <b>GTZAN</b> dataset, believes that this is a <b>" + reply.overall_prediction_class.toUpperCase() +
        "</b> song with a confidence of <b>" + reply.overall_prediction_confidence.toFixed(2) + "%</b>";
    showElement('chart-section');

    loadYTVideo(videoId);

    if (chartUpdater != null) {
        chartUpdater.stop();
        chartUpdater = null;
    }
    chartUpdater = new UpdateChartData(barChart, ytplayer, reply.predictions, 300);
    chartUpdater.start();

    NProgress.done();
    windowScrollTo('ytvideo-section');
}

// Utils
// -----------------------------------------------------------------------------

function setButtonStatus(id, text) { 
    var $btn = $('#' + id);
    $btn.addClass('disabled');
    $btn.text(text);
}

function unsetButtonStatus(id, text) { 
    var $btn = $('#' + id);
    $btn.removeClass('disabled');
    $btn.text(text);
}

function showElement(id) {
  document.getElementById(id).style = "display: block;";
}

function hideElement(id) {
  document.getElementById(id).style = "display: none;";
}

// -----------------------------------------------------------------------------
