import React, { useEffect, useState } from 'react'
import io from 'socket.io-client';

const Reader = () => {

  const [messages, setMessages] = useState([]);
  const socket = io('http://localhost:3000', { transports : ['websocket'] });

  useEffect(() => { 
    socket.on('kafka-message', (message) => {
      setMessages((prevMessages) => [...prevMessages, message]);
    });
  }, []);

  return (
    <div>
      <h2>Kafka Messages:</h2>
      <ul>
          {
            messages.map((message, index) => (
              <li key={index}>{JSON.stringify(message)}</li>
            ))
          }
      </ul>
  </div>
  )
}

export default Reader