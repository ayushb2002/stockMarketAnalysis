import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Chart from "react-apexcharts";
import dayjs from 'dayjs';

const Batch = () => {

    const [data, setData] = useState([]);
    const [RSI, setRSI] = useState([]);
    const [SMA, setSMA] = useState([]);
    const [MFI, setMFI] = useState([]);
    const [MACD, setMACD] = useState([]);
    const [WRM, setWRM] = useState([]);
    const [timeframe, setTimeframe] = useState('1_min');
    const [limitVal, setLimitVal] = useState(10);
    const [indicator, setIndicator] = useState('RSI');
    const candlestickOptions = {
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

        const lineOptions = {
          chart: {
            type: 'line',
            zoom: {
              enabled: true
            }
          },
          title: {
            text: indicator,
            align: 'left'
          },
          dataLabels: {
            enabled: false
          },
          stroke: {
            curve: 'straight'
          },
          xaxis: {
              type: 'category',
              labels: {
                formatter: function(val) {
                  return dayjs(val).format('MMM DD HH:mm')
                }
              }
            },
            grid: {
              row: {
                colors: ['#f3f3f3', 'transparent'],
                opacity: 0.5
              },
            },
          }

      const resetLimit = async (limit) => {
        setData([]);
        setRSI([]);
        setSMA([]);
        setMFI([]);
        setMACD([]);
        setWRM([]);
        const res = await axios.get(`http://127.0.0.1:4000/batch/niftyData/${timeframe}/${limit}`);
        console.log(res);
        res["data"].forEach(el => {
            var obj = {
                x: el['x'].split('+')[0],
                y: el['y']
            }
            var rsi = {
              x: el['x'].split('+')[0],
              y: el['RSI']
            }
            var sma = {
              x: el['x'].split('+')[0],
              y: el['SMA']
            }
            var mfi = {
              x: el['x'].split('+')[0],
              y: el['MFI']
            }
            var macd = {
              x: el['x'].split('+')[0],
              y: el['MACD']
            }
            if(timeframe!='1_min')
            {  
              var wrm = {
                x: el['x'].split('+')[0],
                y: el['WRM']
              }
              setWRM((prevWRM) => [...prevWRM, wrm]);
            }
            setData((prevdata) => [...prevdata, obj]);
            setRSI((prevRSI) => [...prevRSI, rsi]);
            setSMA((prevSMA) => [...prevSMA, sma]);
            setMFI((prevMFI) => [...prevMFI, mfi]);
            setMACD((prevMACD) => [...prevMACD, macd]);
        });
    }

    const resetDataAndLimit = async (tfr) => {
      setData([]);
      setRSI([]);
      setSMA([]);
      setMFI([]);
      setMACD([]);
      setWRM([]);
      const res = await axios.get(`http://127.0.0.1:4000/batch/niftyData/${tfr}/${limitVal}`);
      console.log(res);
      res["data"].forEach(el => {
          var obj = {
              x: el['x'].split('+')[0],
              y: el['y']
          }
          var rsi = {
            x: el['x'].split('+')[0],
            y: el['RSI']
          }
          var sma = {
            x: el['x'].split('+')[0],
            y: el['SMA']
          }
          var mfi = {
            x: el['x'].split('+')[0],
            y: el['MFI']
          }
          var macd = {
            x: el['x'].split('+')[0],
            y: el['MACD']
          }
          if(tfr!='1_min')
          {
            var wrm = {
              x: el['x'].split('+')[0],
              y: el['WRM']
            }
            setWRM((prevWRM) => [...prevWRM, wrm]);
          }
          setData((prevdata) => [...prevdata, obj]);
          setRSI((prevRSI) => [...prevRSI, rsi]);
          setSMA((prevSMA) => [...prevSMA, sma]);
          setMFI((prevMFI) => [...prevMFI, mfi]);
          setMACD((prevMACD) => [...prevMACD, macd]);
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
            <select 
            name="timeframe" 
            onChange={
                (e) => {
                  e.preventDefault();
                  setTimeframe(e.target.value);
                  resetDataAndLimit(e.target.value, '10');
                }
              } 
            className='block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-200 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:max-w-xs sm:text-sm sm:leading-6 mx-5'>
                  <option value="1_min">1 Minute</option>
                  <option value="5_min">5 Minute</option>
                  <option value="15_min">15 Minute</option>
                  <option value="1_hr">1 Hour</option>
                  <option value="1_day">1 Day</option>
                </select>
            <select 
                name="limiting" 
                onChange={
                  (e) => {
                      e.preventDefault();
                      setLimitVal(e.target.value);
                      resetLimit(e.target.value)
                    }
                  } 
                className='block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-200 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:max-w-xs sm:text-sm sm:leading-6'>
                  <option value="10">10</option>
                  <option value="50">50</option>
                  <option value="100">100</option>
                  <option value="500">500</option>
                  <option value="1000">1000</option>
                  <option value="2000">2000</option>
            </select>
            </div>
            <div className='p-10 flex justify-center'>
                <Chart options={candlestickOptions} series={[{name: "candle", data: data}]} type="candlestick" height={500} width={1200} />
            </div>
            <div className='flex justify-end px-5'>
                <select name="indicator" onChange={(e) => {e.preventDefault();setIndicator(e.target.value);}} className='block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-200 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:max-w-xs sm:text-sm sm:leading-6'>
                  <option value="RSI">RSI</option>
                  <option value="SMA">Simple Moving Average</option>
                  <option value="MACD">MACD</option>
                  <option value="MFI">MFI</option>
                  {(timeframe!='1_min') && (
                    <option value="WRM">Weighted RSI-MACD</option>
                  )}
                </select>
            </div>
            <div className='p-10 flex justify-center'>
                <Chart options={lineOptions} series={[
                    {
                      name: "line", 
                      data: indicator === "RSI" ? RSI : indicator === "SMA" ? SMA : indicator === "MFI"? MFI : indicator == "MACD" ? MACD : indicator == "WRM" ? WRM : null,
                    }
                  ]} type="line" height={300} width={1200} />
            </div>
        </div>
    </div>
  )
}

export default Batch
