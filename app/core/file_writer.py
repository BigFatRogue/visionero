import asyncio
import aiofiles
import json
from pathlib import Path

from app.core.config import settings

from app.core.logging import metrics


class AsyncFileWriter:
    def __init__(self):
        self.file_path: Path = Path(settings.DATA_FILEPATH)
        self.flush_interval = settings.FLUSH_INTERVAL

        self.queue: asyncio.Queue = asyncio.Queue()
        self._task: asyncio.Task | None = None
        self._running = False

        self.buffer = []

        self.count_write_message = 0
        
    async def start(self):
        metrics.log_info(f'start {self.__class__.__name__}')
        self._running = True
        self._task = asyncio.create_task(self._writer_loop())
        
    async def stop(self):
        metrics.log_info(f'stop {self.__class__.__name__}')
        self._running = False
        if self._task and not self.queue.empty():
            await self._task
        
    async def write(self, message: dict) -> None:
        await self.queue.put(message)
    
    async def _writer_loop(self):
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.buffer = []
        last_flush = asyncio.get_event_loop().time()
        
        try:
            while self._running or not self.queue.empty():
                try:
                    current_time = asyncio.get_event_loop().time()

                    message = await asyncio.wait_for(self.queue.get(), timeout=self.flush_interval)
                    self.buffer.append(json.dumps(message))
                    
                    if len(self.buffer) >= settings.FLUSH_COUNT or (current_time - last_flush) >= self.flush_interval:
                        await self._flush_buffer(self.buffer)
                        self.buffer.clear()
                        last_flush = current_time
                        
                except asyncio.TimeoutError:
                    if self.buffer:
                        await self._flush_buffer(self.buffer)
                        self.buffer.clear()
                        last_flush = asyncio.get_event_loop().time()
                        
        except Exception as e:
            metrics.log_error("File writer error", e)
    
    async def _flush_buffer(self, buffer: list[str]):
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        
        async with aiofiles.open(self.file_path, 'a') as f:
            await f.write('\n'.join(buffer) + '\n')
        self.count_write_message += len(buffer)
        metrics.log_info('success write file')

    def get_statistics(self) -> dict:
        return {
            'count_write_message': self.count_write_message,
            'count_file_wait_wtrie': len(self.buffer)
        }

async_file_writer = AsyncFileWriter()