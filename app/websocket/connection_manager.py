from fastapi import WebSocket
import asyncio

from app.core.logging import metrics


class ConnectionManager:
    def __init__(self):
        self.source_connection: WebSocket | None = None
        self.frontend_connections: set[WebSocket] = set()

        self.queue: asyncio.Queue[str] =  None
        self._task: asyncio.Task | None = None
        self._running = False

        self.count_send_message = 0
    
    async def start(self):
        if self._running: return
        
        metrics.log_info(f'start {self.__class__.__name__}')
        self._running = True
        self.queue = asyncio.Queue()
        self._task = asyncio.create_task(self._broadcast_loop())
        
    async def stop(self):
        metrics.log_info(f'stop {self.__class__.__name__}')
        self._running = False

        if self._task and not self.queue.empty():
            await self._task
        self.queue = None

    async def connect_source(self, websocket: WebSocket):
        await websocket.accept()
        self.source_connection = websocket
    
    def disconnect_source(self):
        self.source_connection = None

    async def connect_frontend(self, websocket: WebSocket):
        await websocket.accept()
        self.frontend_connections.add(websocket)
    
    def disconnect_frontend(self, websocket: WebSocket):
        self.frontend_connections.discard(websocket)
    
    async def broadcast_to_frontend(self, message:str):
        await self.queue.put(message)

    async def _broadcast_loop(self):
        while self._running or (self.queue and not self.queue.empty()):
            try:
                message = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                await self._broadcast_to_frontend(message)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                metrics.log_error('error send messge frontend', e)

    async def _broadcast_to_frontend(self, message: str):
        disconnected = set()
        for connection in self.frontend_connections:
            try:
                await connection.send_text(message)
                self.count_send_message += 1
            except Exception as e:
                metrics.log_error('error send messge frontend', e)
                disconnected.add(connection)
        
        for connection in disconnected:
            self.frontend_connections.discard(connection)
    
    def get_statistics(self) -> dict:
        return {
            'count_send_message': self.count_send_message,
            'count_connection_frontend': len(self.frontend_connections),
            'count_message_wait_send': self.queue.qsize() if self.queue is not None else 0
        }


connection_manager = ConnectionManager()