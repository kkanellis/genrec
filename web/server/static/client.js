//var connection = new WebSocket('ws://0.0.0.0:8080');
var connection = new WebSocket("ws://localhost:8080/ws")

// When the connection is open, send some data to the server
connection.onopen = function () {
  var youtube_link = 'https://www.youtube.com/watch?v=nppKPgdc_u0';

  // Construct an object to test if server knows when to predict a song
  var user_preferences = {
    "request_type" : "predict",
    "dataset" : "gtzan",
    "classifiers": "kNN_5",
    "videoId" : "Ids34fx9", // Arbitrary stuff for now: Must be replaced with process of ydl.download
  };

  //connection.send(JSON.stringify(user_preferences)); // Send the message to the server
  connection.send(youtube_link); // Send the message to the server

};

// Log errors
connection.onerror = function (error) {
  console.log('WebSocket Error ' + error);
};

// Log messages from the server
connection.onmessage = function (e) {
  console.log('Server: ' + e.data);
};
