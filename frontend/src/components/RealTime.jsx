import React, { useEffect, useState } from 'react'
import io from 'socket.io-client';
import Chart from "react-apexcharts";
import dayjs from 'dayjs';

const RealTime = () => {

  const [data, setData] = useState([]);
  const [category, setCategory] = useState('1_min');
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
    socket.on(`kafka-message-${category}`, (message) => {
      message = JSON.parse(message);
      var obj = {
        x: message['date'].split('+')[0],
        y: [message['open'], message['high'], message['low'], message['close']]
      }
      setData((prevdata) => [...prevdata, obj]);
    });
    return () => {
      socket.disconnect();
    }
  }, [category]);

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
      <div className='flex justify-end px-5'>
                <select 
                  name="categoryFilter" 
                  onChange={
                    (e) => {
                      e.preventDefault();
                      setCategory(e.target.value);
                      setData([]);
                      }
                    } 
                  className='block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-200 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:max-w-xs sm:text-sm sm:leading-6'>
                      <option value="1_min">1 Minute</option>
                      <option value="5_min">5 Minutes</option>
                      <option value="15_min">15 Minutes</option>
                      <option value="1_hour">1 Hour</option>
                      <option value="1_day">1 Day</option>
                </select>
            </div>
      <div className='p-10 flex justify-center'>
          <Chart options={options} series={[{data: data}]} type="candlestick" height={700} width={1200} />
      </div>
      </div>  
    </div>
  )
}

export default RealTime