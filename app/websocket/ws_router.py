from fastapi import WebSocket, WebSocketDisconnect, APIRouter
import asyncio

from app.core.process_data import process_data
from app.core.logging import metrics

from app.core.file_writer import async_file_writer

from app.websocket.connection_manager import connection_manager


ws_router = APIRouter(prefix='/ws', tags=['WebSocket'])


@ws_router.websocket('/source')
async def source(websocket: WebSocket) -> None:
    retry = 0
    max_retry = 5
    
    while retry < max_retry:
        try:
            await connection_manager.connect_source(websocket)
            metrics.log_info('websocket source connect')

            while True:
                data = await websocket.receive_text()
                processed = process_data(data)
                message_json = processed.to_json()
                
                if message_json is not None:
                    await connection_manager._broadcast_to_frontend(message_json)
                    await async_file_writer.write(message_json)

        except WebSocketDisconnect:
            connection_manager.disconnect_source()
            metrics.log_info('websocket source disconnect')
            break
        except Exception as e:
            retry += 1
            metrics.log_error(f'websocket source error: {e}')
            await asyncio.sleep(1)


@ws_router.websocket('/frontend')
async def frontend(websocket: WebSocket) -> None:
    retry = 0
    max_retry = 5
    
    while retry < max_retry:
        try:
            await connection_manager.connect_frontend(websocket) 
            metrics.log_info('websocket frontend connect')

            while True:
                await websocket.receive_text()
            
        except WebSocketDisconnect:
            connection_manager.disconnect_frontend(websocket)
            metrics.log_info('websocket source disconnect')
            break
        except Exception as e:
            retry += 1
            metrics.log_error(f'websocket frontend error: {e}')
            await asyncio.sleep(1)