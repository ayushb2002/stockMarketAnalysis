import React, { useEffect, useState } from 'react';
import { Kafka } from 'kafkajs';

const Consumer = () => {
    const kafka = new Kafka({
        clientId: 'stocks',
        brokers: ['kafka:9092'],
      })
    
    const [data, setData] = useState('');

    useEffect(() => {
        const kafkaConn = async () => {
            const consumer = kafka.consumer({ groupId: 'stocks-group' })
            await consumer.connect()
            await consumer.subscribe({ topic: 'NiftyStream', fromBeginning: true })

            await consumer.run({
            eachMessage: async ({ topic, partition, message }) => {
                console.log({
                value: message.value.toString(),
                })
                setData(message.value.toString());
                },
            })  
        }

        kafkaConn();
      }, [])
      

  return (
    <div>
      {data}
    </div>
  )
}

export default Consumer
