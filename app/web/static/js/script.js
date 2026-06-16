let lastMessage = ''
const textViewer = document.querySelector('.viewer__text')
const btnUpdate = document.querySelector('.viewer__btn-update')

const ws = new WebSocket('ws://localhost:8000/ws/frontend')

ws.addEventListener('message', (event) => {
    const data = JSON.parse(event.data)
    
    lastMessage = ''
    for (const [key, value] of Object.entries(data)) {
        lastMessage += `<div class="row"><span class="key">${key}:</span> <span>${value}</span></div>`
    }

    if (lastMessage === '') textViewer.innerHTML = lastMessage
})

btnUpdate.addEventListener('click', () => {
    textViewer.childNodes.forEach(element => {
        element.remove()
    });
    textViewer.innerHTML = lastMessage
})
