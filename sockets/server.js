const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const kafka = require('kafka-node');
const cors = require('cors');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);
app.use(cors()); 

const Consumer = kafka.Consumer;
const client = new kafka.KafkaClient('kafka:9092');
const consumer = new Consumer(client, [{ topic: 'NiftyStream', partition: 0 }, { topic: 'NiftyStream', partition: 1 }, { topic: 'NiftyStream', partition: 2 }], {
  autoCommit: false,
});

// WebSocket connection
io.on('connection', (socket) => {
  console.log('WebSocket connected');

  consumer.on('message', (message) => {
    obj = JSON.parse(message['value']);
    obj2 = JSON.parse(obj);
    console.log(obj2);
    socket.emit(`kafka-message-${obj2['timeframe']}`, obj);
  });
});

server.listen(3000, () => {
  console.log('Server is running on http://localhost:3000');
});