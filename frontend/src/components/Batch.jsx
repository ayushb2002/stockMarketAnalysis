import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Chart from "react-apexcharts";
import dayjs from 'dayjs';

const Batch = () => {

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

      const resetLimit = async (limit) => {
        setData([]);
        const res = await axios.get(`http://127.0.0.1:4000/batch/niftyData/${limit}`);
        res["data"].forEach(el => {
            var obj = {
                x: el['x'].split('+')[0],
                y: el['y']
            }
            setData((prevdata) => [...prevdata, obj]);
        });
    }

    useEffect(() => {
        resetLimit(10);
    }, [])
    

  return (
    <div className='grid grid-cols-5 min-h-[100vh]'>
        <div className='p-10 bg-cyan-950 text-white text-xl'>
            <div className='p-5'>
                <a href="/"><span>Home</span></a>
            </div>
            <div className='p-5'>
                <a href="/realtime"><span>Nifty 50 Real Time</span></a>
            </div>
            <div className='p-5'>
                <a href="/batch"><span className='font-bold'>Nifty 50 Batch Data</span></a>
            </div>
        </div>
        <div className='col-span-4'>
            <div className='p-10 flex justify-center'>
                <span className='text-2xl'>Batch Data</span>
            </div>
            <div className='flex justify-end px-5'>
                <select name="limiting" onChange={(e) => {e.preventDefault();resetLimit(e.target.value)}} className='block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-200 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:max-w-xs sm:text-sm sm:leading-6'>
                  <option value="10" selected>10</option>
                  <option value="50">50</option>
                  <option value="100">100</option>
                  <option value="500">500</option>
                  <option value="1000">1000</option>
                  <option value="2000">2000</option>
                </select>
            </div>
            <div className='p-10 flex justify-center'>
                <Chart options={options} series={[{name: "candle", data: data}]} type="candlestick" height={700} width={1200} />
            </div>
        </div>
    </div>
  )
}

export default Batch
