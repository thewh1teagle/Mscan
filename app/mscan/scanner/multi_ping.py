from icmplib import async_multiping


class MultiPinger:
    """ Multithreaded class for pinging hosts and display progress """

    @staticmethod
    async def ping(ips):
        return await async_multiping(ips, count=1, timeout=1, privileged=False)
