#Ans
#Wed Aug 23 14:15:44 2023 Producer: Running
#Wed Aug 23 14:15:44 2023 Consumer: Running
#Wed Aug 23 14:15:45 2023 >got 0.7521992951929961
#Wed Aug 23 14:15:46 2023 >got 0.6902329608823723
#Wed Aug 23 14:15:46 2023 >got 0.7563192053926513
#Wed Aug 23 14:15:47 2023 >got 0.20394526742250085
#Wed Aug 23 14:15:48 2023 >got 0.865895603636071
#Wed Aug 23 14:15:48 2023 >got 0.17573299334653703
#Wed Aug 23 14:15:49 2023 >got 0.9342241227360417
#Wed Aug 23 14:15:50 2023 >got 0.9905831045898115
#Wed Aug 23 14:15:50 2023 >got 0.3089882438406426
#Wed Aug 23 14:15:50 2023 Producer: Done
#Wed Aug 23 14:15:50 2023 >got 0.21278960332859553
#Wed Aug 23 14:15:50 2023 Consumer: Done

# we will create a producer coroutine that will generate ten random numbers 
# and put them on the queue. We will also create a consumer coroutine 
# that will get numbers from the queue and report their values.

from random import random
import asyncio
import time

# coroutine to generate work
async def producer(queue):
    print (f'{time.ctime()} Producer: Running')
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
    print(f'{time.ctime()} Consumer: Running')
    # consume work
    while True:
        # get a unit of work
        item = await queue.get()
        # check for stop signal
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
