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
const consumer = new Consumer(client, [{ topic: 'StockStream', partition: 0 }, { topic: 'StockStream', partition: 1 }, { topic: 'StockStream', partition: 2 }], {
  autoCommit: false,
});

// WebSocket connection
io.on('connection', (socket) => {
  console.log('WebSocket connected');

  consumer.on('message', (message) => {
    obj = JSON.parse(message['value']);
    console.log(obj);
    socket.emit('kafka-message', obj);
  });
});

server.listen(3000, () => {
  console.log('Server is running on http://localhost:3000');
});