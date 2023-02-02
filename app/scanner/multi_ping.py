from typing import List
from icmplib import async_ping
import threading
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

class MultiPinger(threading.Thread):
    """ Multithreaded class for pinging hosts and display progress """
    def __init__(self) -> None:
        self._running = False
        self._progress = 0
        self._ips = None
        self._hosts: List[str] = []
        self._lock = threading.Lock()
        threading.Thread.__init__(self)

    def set_ips(self, ips):
        self._ips = ips

    @property
    def is_running(self):
        with self._lock:
            return self._running
    
    def progress(self):
        with self._lock:
            return self._progress
    
    def hosts(self):
        with self._lock:
            return self._hosts

    def run(self):
        if self._ips is None:
            raise Exception("You havn't setted ips using set_ips")
        with self._lock:
            self._progress = 0
            self._running = True
        total = len(self._ips)
        self.hosts = asyncio.run(async_multiping(self._ips, count=1, timeout=0.5, progress_callback=lambda a,b: print(a,b)))
        

