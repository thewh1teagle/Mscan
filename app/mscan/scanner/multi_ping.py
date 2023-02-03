from typing import List
from icmplib import async_ping
import asyncio

async def async_multiping(addresses, count=2, interval=0.5, timeout=2,
        concurrent_tasks=50, source=None, family=None, privileged=True, progress_callback = None):

    loop = asyncio.get_running_loop()
    tasks = []
    tasks_pending = set()
    total = len(addresses)

    for i, address in enumerate(addresses):
        if len(tasks_pending) >= concurrent_tasks:
            _, tasks_pending = await asyncio.wait(
                tasks_pending,
                return_when=asyncio.FIRST_COMPLETED)
        
        if progress_callback:
            progress_callback(i, total)

        task = loop.create_task(
            async_ping(
                address=address,
                count=count,
                interval=interval,
                timeout=timeout,
                source=source,
                family=family,
                privileged=privileged,
                ))

        tasks.append(task)
        tasks_pending.add(task)

    await asyncio.wait(tasks_pending)

    return [task.result() for task in tasks]

class MultiPinger:
    """ Multithreaded class for pinging hosts and display progress """

    def progress_cb(self, finished, total):
        # print(f'total: {total} finished: {finished}')
        self._progress = finished / total * 100

    async def ping(self, ips):
        return await async_multiping(ips, count=1, timeout=0.5, progress_callback=self.progress_cb, privileged=False)
        

