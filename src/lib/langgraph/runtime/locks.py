import asyncio

ThreadID = str


class ThreadLockManager:
    """thread 단위 실행 락 관리자"""

    def __init__(self) -> None:
        self._locks: dict[ThreadID, asyncio.Lock] = {}

    async def acquire(self, thread_id: ThreadID) -> None:
        lock = self._locks.setdefault(thread_id, asyncio.Lock())
        await lock.acquire()

    def release(self, thread_id: ThreadID) -> None:
        lock = self._locks.get(thread_id)
        if lock and lock.locked():
            lock.release()
