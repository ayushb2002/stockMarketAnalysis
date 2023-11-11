import React, { useEffect, useState } from 'react'
import io from 'socket.io-client';
import Chart from "react-apexcharts";
import dayjs from 'dayjs';

const RealTime = () => {

  const [data, setData] = useState([]);
  const options = {
    chart: {
      type: 'candlestick'
    },
    title: {
      text: 'Nifty 50 Data',
      align: 'left'
    },
    xaxis: {
      type: 'category',
      labels: {
        formatter: function(val) {
          return dayjs(val).format('MMM DD HH:mm')
        }
      }
    },
    yaxis: {
      tooltip: {
        enabled: true
      }
    }
  }
  const socket = io('http://localhost:3000', { transports : ['websocket'] });

  useEffect(() => { 
    socket.on('kafka-message', (message) => {
      message = JSON.parse(message);
      message = JSON.parse(message);
      var obj = {
        x: message['date'].split('+')[0],
        y: [message['open'], message['high'], message['low'], message['close']]
      }
      setData((prevdata) => [...prevdata, obj]);
    });
  }, []);

  return (
    <div className='grid grid-cols-5 min-h-[100vh]'>
      <div className='p-10 bg-cyan-950 text-white text-xl'>
        <div className='p-5'>
          <a href="/"><span>Home</span></a>
        </div>
        <div className='p-5'>
          <a href="/realtime"><span className='font-bold'>Nifty 50 Real Time</span></a>
        </div>
        <div className='p-5'>
          <a href="/batch"><span>Nifty 50 Batch Data</span></a>
        </div>
      </div>
      <div className='col-span-4'>
      <div className='p-10 flex justify-center'>
                <span className='text-2xl'>Real Time Data</span>
            </div>
        <div className='p-10 flex justify-center'>
          <Chart options={options} series={[{data: data}]} type="candlestick" height={700} width={1200} />
        </div>
      </div>  
    </div>
  )
}

export default RealTime