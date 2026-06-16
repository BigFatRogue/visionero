const ws = new WebSocket('ws://localhost:8000/ws/frontend')

ws.addEventListener('message', (event) => {
    const data = JSON.parse(event.data)
    if (data['sensor_id'] === 'sensor_1') {
        const {value, moving_average} = data
        console.log(value, moving_average)
    }
})

