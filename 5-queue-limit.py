#Ans
#Wed Aug 23 15:02:09 2023 Consumer: Running
#Wed Aug 23 15:02:09 2023 Producer: Running
#Wed Aug 23 15:02:09 2023 Producer: Running
#Wed Aug 23 15:02:09 2023 Producer: Running
#Wed Aug 23 15:02:09 2023 Producer: Running
#Wed Aug 23 15:02:09 2023 Producer: Running
#Wed Aug 23 15:02:09 2023 >got 0.13081372920338274
#Wed Aug 23 15:02:09 2023 >got 0.49787306080306803
#Wed Aug 23 15:02:09 2023 >got 0.0026428132443022667
#Wed Aug 23 15:02:09 2023 >got 0.5958256161861766
#Wed Aug 23 15:02:10 2023 >got 0.2016394465999879
#Wed Aug 23 15:02:10 2023 >got 0.2547819592342857
#Wed Aug 23 15:02:10 2023 >got 0.5455897797688369
#Wed Aug 23 15:02:11 2023 >got 0.06124646920061905
#Wed Aug 23 15:02:11 2023 >got 0.31566008290774505
#Wed Aug 23 15:02:11 2023 >got 0.9038822830123296
#Wed Aug 23 15:02:12 2023 >got 0.8064395536194195
#Wed Aug 23 15:02:13 2023 >got 0.054968719871747784
#Wed Aug 23 15:02:13 2023 >got 0.7789823151737483
#Wed Aug 23 15:02:14 2023 >got 0.6818139031913919
#Wed Aug 23 15:02:15 2023 >got 0.8733903469936938
#Wed Aug 23 15:02:16 2023 >got 0.5421394030643633
#Wed Aug 23 15:02:16 2023 >got 0.8130779635190315
#Wed Aug 23 15:02:17 2023 >got 0.5318205055824126
#Wed Aug 23 15:02:17 2023 >got 0.4079322049948786
#Wed Aug 23 15:02:18 2023 >got 0.0015623835226675764
#Wed Aug 23 15:02:18 2023 >got 0.8478615288561616
#Wed Aug 23 15:02:19 2023 >got 0.2920410787199299
#Wed Aug 23 15:02:19 2023 >got 0.7286137594184733
#Wed Aug 23 15:02:20 2023 >got 0.4507519827649542
#Wed Aug 23 15:02:20 2023 >got 0.5217081176123768
#Wed Aug 23 15:02:21 2023 >got 0.3065955538345386
#Wed Aug 23 15:02:21 2023 >got 0.31209479571918475
#Wed Aug 23 15:02:21 2023 >got 0.17212937891757085
#Wed Aug 23 15:02:22 2023 >got 0.6978338237636535
#Wed Aug 23 15:02:22 2023 >got 0.14830493713980064
#Wed Aug 23 15:02:22 2023 >got 0.2498059561644016
#Wed Aug 23 15:02:23 2023 >got 0.035038081827202916
#Wed Aug 23 15:02:23 2023 >got 0.7601626485817262
#Wed Aug 23 15:02:23 2023 >got 0.804022216849801
#Wed Aug 23 15:02:24 2023 >got 0.23509500628535396
#Wed Aug 23 15:02:25 2023 >got 0.17995833190442423
#Wed Aug 23 15:02:25 2023 Producer0: Done
#Wed Aug 23 15:02:25 2023 >got 0.48388504990691317
#Wed Aug 23 15:02:25 2023 >got 0.79967838825406
#Wed Aug 23 15:02:26 2023 >got 0.9786171096241943
#Wed Aug 23 15:02:27 2023 >got 0.7322847729596828
#Wed Aug 23 15:02:28 2023 >got 0.8368477583374417
#Wed Aug 23 15:02:29 2023 >got 0.7341911805698864
#Wed Aug 23 15:02:29 2023 >got 0.80053427228037
#Wed Aug 23 15:02:30 2023 >got 0.014111411639997073
#Wed Aug 23 15:02:30 2023 Producer1: Done
#Wed Aug 23 15:02:30 2023 >got 0.879675207621136
#Wed Aug 23 15:02:30 2023 Producer2: Done
#Wed Aug 23 15:02:31 2023 >got 0.43304705474519467
#Wed Aug 23 15:02:31 2023 >got 0.4122725266909669
#Wed Aug 23 15:02:31 2023 Producer3: Done
#Wed Aug 23 15:02:32 2023 >got 0.38947991436851404
#Wed Aug 23 15:02:32 2023 Producer4: Done
#Wed Aug 23 15:02:32 2023 >got 0.13141227499815333
#Wed Aug 23 15:02:32 2023 >got 0.13964869655789203

from random import random
import asyncio
import time

# coroutine to generate work
async def producer(queue,id):
    print (f'{time.ctime()} Producer: Running')
    # generate work
    for i in range(10):
        # generate a value
        value = random()
        # block to simulate work
        await asyncio.sleep((id+1)*0.1)
        # add to the queue, may block
        await queue.put(value)
    print(f'{time.ctime()} Producer{id}: Done')

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
        # mark as completed
        queue.task_done()
    # all done
    print(f'{time,ctime()} Consumer: Done')

# entry point coroutine
async def main():
    # create the shared queue
    queue = asyncio.Queue(2)
    # start the consumer
    _ = asyncio.create_task(consumer(queue))
    # create many producers
    producers = [producer(queue,i) for i in range(5)]
    # run and wait for the producers to finish
    await asyncio.gather(*producers)
    # wait for the consumer to process all items
    await queue.join()

# start the asyncio program
asyncio.run(main())