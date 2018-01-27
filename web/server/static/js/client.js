//var connection = new WebSocket('ws://0.0.0.0:8080');
var connection = new WebSocket("ws://localhost:8080/ws")

// When the connection is open, send some data to the server
connection.onopen = function () {
  var youtube_link = 'https://www.youtube.com/watch?v=nppKPgdc_u0';

  var validate_url = {
    "command" : "validate-url",
    "url" : youtube_link,
  };

  // Construct an object to test if server knows when to predict a song
  var user_preferences = {
    "command" : "predict",
    "dataset" : "gtzan",
    "classifiers": "kNN_5",
    "videoId" : "Ids34fx9", // Arbitrary stuff for now: Must be replaced with process of ydl.download
  };

  connection.send(JSON.stringify(validate_url)); // Send the message to the server
};

// Log errors
connection.onerror = function (error) {
  console.log('WebSocket Error ' + error);
};

// Log messages from the server
connection.onmessage = function (e) {
  reply = JSON.parse(e.data)
  
  if (reply.command == 'OK') {
    console.info('Server: ' + reply.message);
  }
  else if (reply.command == 'ERROR') {
    console.error('Server: ' + reply.message);
  }
  else if (reply.command == 'prediction') {
   
  }
  else
    console.error('Invalid command received: ' + reply.command);
  }
};
