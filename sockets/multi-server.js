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

const topics = ['OneMinStream', 'FiveMinStream', 'FifteenMinStream', 'OneHrStream', 'OneDayStream'];

// Create a single consumer for all topics
const consumer = new Consumer(client, topics.map(topic => ({ topic, partition: 0 }, { topic, partition: 1 }, { topic, partition: 2 })), { autoCommit: false });

// WebSocket connection
io.on('connection', (socket) => {
  console.log('WebSocket connected');

  // Set up message event listener for the single consumer
  consumer.on('message', (message) => {
    const obj = JSON.parse(message['value']);
    const topic = message['topic'];
    console.log(topic);
    console.log(obj);
    console.log('_______');
    socket.emit(`kafka-message-${topic}`, obj);
  });
});

server.listen(3000, () => {
  console.log('Server is running on http://localhost:3000');
});
