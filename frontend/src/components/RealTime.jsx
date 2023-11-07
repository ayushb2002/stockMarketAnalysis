import React, { useEffect, useState } from 'react'
import io from 'socket.io-client';
import Chart from "react-apexcharts";

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
      type: 'datetime'
    },
    yaxis: {
      tooltip: {
        enabled: true
      }
  }}
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

          <Chart options={options} series={[{data: data}]} type="candlestick" height={600} width={1100} />

        </div>
        <div className='p-10 flex justify-center'>
          <table className='table-auto'>
            <thead>
              <tr>
                <th>Date</th>
                <th>Open</th>
                <th>High</th>
                <th>Low</th>
                <th>Close</th>
              </tr>
            </thead>
            <tbody>
            {
              data.map((dp, index) => (
                <tr key={index}>
                  <td>{dp.x}</td>
                  <td>{dp.y[0]}</td>
                  <td>{dp.y[1]}</td>
                  <td>{dp.y[2]}</td>
                  <td>{dp.y[3]}</td>
                </tr>
              ))
            }
            </tbody>
          </table>

        </div>
      </div>  
    </div>
  )
}

export default RealTime

{/* 

*/}