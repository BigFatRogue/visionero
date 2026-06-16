import argparse
import asyncio
import random
from datetime import datetime, UTC
from time import time
import json
from websockets import connect


def generator_id(sensors_count: int) -> int:
    return f"sensor_{random.randint(1, sensors_count)}"

def generator_message(sensors_count: int, bad_rate: float) -> dict:
    data = {
        "sensor_id": generator_id(sensors_count),
        "timestamp": datetime.now(UTC).isoformat(timespec='milliseconds'),
        "value": round(random.uniform(-42, 42), 2)
    }

    if random.random() < bad_rate:
        data['value'] = None
    
    return data

async def send_messages(uri: str, count: int, rps: int, sensors: int, bad_rate: float):
    delay = 1 / rps if rps > 0 else 0
    sent_message = 0
    statistics = {}
    start_time = time()    
    
    async with connect(uri) as websocket:
        for _ in range(count):
            message = generator_message(sensors, bad_rate)
            await websocket.send(json.dumps(message))
            sent_message += 1

            if delay > 0:
                await asyncio.sleep(delay)
            calc_statistic(message, statistics)
                
    end_time = time() - start_time
    
    print()
    print(f'Отправлено {sent_message} сообщений за {end_time:.2f} секунд')
    print(f'Фактический RPS: {sent_message/end_time:.2f}')
    
    for sid in sorted(statistics):
        message = statistics[sid]
        print(f"Sensor: <{sid}>. Количество сообщений: {message['count_message']}; количество повреждённых сообщений: {message['count_bad_message']}.")
    
def calc_statistic(message: dict, statistics: dict) -> None:
    value: dict = statistics.setdefault(
        message['sensor_id'], 
        {'count_message': 0, 'count_bad_message': 0}
    )

    value['count_message'] += 1

    if message['value'] is None:
        value['count_bad_message'] += 1
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--count', type=int, required=True)
    parser.add_argument('--rps', type=int, required=True)
    parser.add_argument('--sensors', type=int, default=5)
    parser.add_argument('--bad-rate', type=float, default=0.0)
    parser.add_argument('--uri', type=str, default='ws://localhost:8000/ws/source')

    args = parser.parse_args()

    asyncio.run(send_messages(
        uri=args.uri,
        count=args.count,
        rps=args.rps,
        sensors=args.sensors,
        bad_rate=args.bad_rate
    ))


if __name__ == "__main__":
    main()


    
    
    
    

