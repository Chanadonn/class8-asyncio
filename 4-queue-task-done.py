#Ans
#Wed Aug 23 14:40:33 2023 Consumer: Running
#Wed Aug 23 14:40:33 2023 Producer: Running
#Wed Aug 23 14:40:34 2023 >got 0.5125371901690837
#Wed Aug 23 14:40:35 2023 >got 0.8382706524802412
#Wed Aug 23 14:40:36 2023 >got 0.6030315251735197
#Wed Aug 23 14:40:36 2023 >got 0.8980689197406764
#Wed Aug 23 14:40:37 2023 >got 0.045068065605868846
#Wed Aug 23 14:40:37 2023 >got 0.24810403525162616
#Wed Aug 23 14:40:37 2023 >got 0.5342119334084011
#Wed Aug 23 14:40:38 2023 >got 0.8278375751460212
#Wed Aug 23 14:40:39 2023 >got 0.9172268007519934
#Wed Aug 23 14:40:39 2023 Producer: Done
#Wed Aug 23 14:40:40 2023 >got 0.13952571903096578

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
    print(f'{time.ctime()} Producer: Done')
# coroutine to consume work
async def consumer(queue):
    print(f'{time.ctime()} Consumer: Running')
    # consume work
    while True:
        # get a unit of work
        item = await queue.get()
        # report
        print(f'{time.ctime()} >got {item}')
        # block while processing
        if item:
            await asyncio.sleep(item)
        # mark the task as done
        queue.task_done()

# entry point coroutine
async def main():
    # create the shared queue
    queue = asyncio.Queue()
    # start the consumer
    _ = asyncio.create_task(consumer(queue))
    # start the producer and wait for it to finish
    await asyncio.create_task(producer(queue))
    # wait for all itens to be processed
    await queue.join()

# start the asyncio program
asyncio.run(main())