var connection = new WebSocket('ws://0.0.0.0:8080');

// When the connection is open, send some data to the server
connection.onopen = function () {
  connection.send('Ping re mofo'); // Send the message 'Ping' to the server
};

// Log errors
connection.onerror = function (error) {
  console.log('WebSocket Error ' + error);
};

// Log messages from the server
connection.onmessage = function (e) {
  console.log('Server: ' + e.data);
};
