import React from 'react'

const Home = () => {
  return (
    <div className='grid grid-cols-5 min-h-[100vh]'>
      <div className='p-10 bg-cyan-950 text-white text-xl'>
        <div className='p-5'>
          <a href="/"><span className='font-bold'>Home</span></a>
        </div>
        <div className='p-5'>
          <a href="/realtime"><span>Nifty 50 Real Time</span></a>
        </div>
        <div className='p-5'>
          <a href="/batch"><span>Nifty 50 Batch Data</span></a>
        </div>
      </div>
      <div className='col-span-4'>
        
      </div>  
    </div>
  )
}

export default Home
