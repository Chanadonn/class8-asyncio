#Ans
#Producer: Running
#Wed Aug 23 14:31:43 2023 Consumer: Running
#Wed Aug 23 14:31:44 2023 >got 0.18547799301451118
#Wed Aug 23 14:31:44 2023 >got 0.29647412042524934
#Wed Aug 23 14:31:44 2023 >got 0.29943222893760435
#Wed Aug 23 14:31:45 2023 Consumer: gave up waiting...
#Wed Aug 23 14:31:45 2023 >got 0.7334393149888581
#Wed Aug 23 14:31:46 2023 Consumer: gave up waiting...
#Wed Aug 23 14:31:46 2023 >got 0.5152546060840819
#Wed Aug 23 14:31:46 2023 >got 0.4598642062077474
#Wed Aug 23 14:31:46 2023 >got 0.25579522747923067
#Wed Aug 23 14:31:47 2023 Consumer: gave up waiting...
#Wed Aug 23 14:31:47 2023 >got 0.8141124060054741
#Wed Aug 23 14:31:48 2023 Consumer: gave up waiting...
#Wed Aug 23 14:31:48 2023 >got 0.7701149794046923
#Wed Aug 23 14:31:48 2023 Consumer: gave up waiting...
#Wed Aug 23 14:31:49 2023 Producer: Done
#Wed Aug 23 14:31:49 2023 >got 0.963487093380032
#Consumer: Done

from random import random
import asyncio
import time

# coroutine to generate work
async def producer(queue):
    print ('Producer: Running')
    # generate work
    for i in range(10):
        # generate a value
        value = random()
        # block to simulate work
        await asyncio.sleep(value)
        # add to the queue
        await queue.put(value)
    # send an all done signal
    await queue.put(None)
    print(f'{time.ctime()} Producer: Done')
# consume work
async def consumer(queue):
    print(f'{time.ctime()} Consumer: Running')
    # consume work
    while True:
        # get a unit of work
        try:
            # retrieve the get() awaitable
            get_await = queue.get()
            # await the awaitable with a timeout
            item = await asyncio.wait_for(get_await, 0.5)
        except asyncio.TimeoutError:
            print(f'{time.ctime()} Consumer: gave up waiting...')
            continue
        # check for stop
        if item is None:
            break
        # report
        print(f'{time.ctime()} >got {item}')
    # all done
    print('Consumer: Done')

# entry point coroutine
async def main():
    # create the shared queue
    queue = asyncio.Queue()
    # run the producer and cosumers
    await asyncio.gather(producer(queue), consumer(queue))

# start the asyncio program
asyncio.run(main())