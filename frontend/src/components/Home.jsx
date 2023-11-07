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
      <div className='col-span-4 grid grid-cols-5'>
        <div></div>
        <div className='col-span-3 text-center'>
          <div className='p-10'>
            <span className='text-3xl'>Trading Analysis</span>
          </div>
          <div className='p-10'>
            <img src="https://learn.g2.com/hubfs/Imported%20sitepage%20images/1ZB5giUShe0gw9a6L69qAgsd7wKTQ60ZRoJC5Xq3BIXS517sL6i6mnkAN9khqnaIGzE6FASAusRr7w=w1439-h786.png" alt="#" className='w-[50vw]' />
          </div>
        </div>
        <div></div>
      </div>  
    </div>
  )
}

export default Home
