#Ans
#Producer: Running
#Consumer: Running
#Wed Aug 23 14:24:11 2023 Consumer: got noting, waiting a while...
#Wed Aug 23 14:24:12 2023 Consumer: got noting, waiting a while...
#Wed Aug 23 14:24:12 2023 >got 0.8957375289996109
#Wed Aug 23 14:24:12 2023 >got 0.009933400442861062
#Wed Aug 23 14:24:12 2023 Consumer: got noting, waiting a while...
#Wed Aug 23 14:24:13 2023 >got 0.45560452166600307
#Wed Aug 23 14:24:13 2023 Consumer: got noting, waiting a while...
#Wed Aug 23 14:24:13 2023 >got 0.21950831038666607
#Wed Aug 23 14:24:13 2023 >got 0.24261161816365062
#Wed Aug 23 14:24:13 2023 Consumer: got noting, waiting a while...
#Wed Aug 23 14:24:14 2023 >got 0.3263934945365574
#Wed Aug 23 14:24:14 2023 Consumer: got noting, waiting a while...
#Wed Aug 23 14:24:14 2023 >got 0.4530440010707538
#Wed Aug 23 14:24:14 2023 >got 0.028036112764123544
#Wed Aug 23 14:24:14 2023 >got 0.11221575921323923
#Wed Aug 23 14:24:14 2023 Consumer: got noting, waiting a while...
#Wed Aug 23 14:24:15 2023 Consumer: got noting, waiting a while...
#Wed Aug 23 14:24:15 2023 Producer: Done
#Wed Aug 23 14:24:16 2023 >got 0.9032562926132427
#Wed Aug 23 14:24:16 2023 Consumer: Done

from random import random
import asyncio
import time

# coroutine to generate work
async def producer(queue):
    print (f'Producer: Running')
    # generate work
    for i in range(10):
        # generate a value
        value = random()
        # block to simulate work
        await asyncio.sleep(value)
        # add to the queue
        await queue.put(value)
        # print(f'{time.ctime()} Producer: put {value}')
    # send an all done signal
    await queue.put(None)
    print(f'{time.ctime()} Producer: Done')
# coroutine to consume work
async def consumer(queue):
    print(f'Consumer: Running')
    # consume work
    while True:
        # get a unit of work without blocking
        try:
            item = queue.get_nowait()
        except asyncio.QueueEmpty:
            print(f'{time.ctime()} Consumer: got noting, waiting a while...')
            await asyncio.sleep(0.5)
            continue
        # check for stop
        if item is None:
            break
        # report
        print(f'{time.ctime()} >got {item}')
    # all done
    print(f'{time.ctime()} Consumer: Done')

# entry point coroutine
async def main():
    # create the shared queue
    queue = asyncio.Queue()
    # run the producer and cosumers
    await asyncio.gather(producer(queue), consumer(queue))

# start the asyncio program
asyncio.run(main())