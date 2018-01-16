import asyncio
import os

import aiohttp.web

# Bind to 0.0.0.0:8080
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 8080))

'''
    The websocket handler handles all requests under '/'
    Also, it prints all messages that gets from the client
    If message is 'close', the websocket closes.
'''
async def websocket_handler(request):
    print('Websocket connection starting')
    ws = aiohttp.web.WebSocketResponse() # Creates websocket in request
    await ws.prepare(request)
    print('Websocket connection ready')


    async for msg in ws: # while loop
        print(msg)
        if msg.type == aiohttp.WSMsgType.TEXT:
            print(msg.data) # Server echos each message that get from client in terminal
            if msg.data == 'close': # If client sends 'close', websocket closes
                await ws.close()
            else:
                await ws.send_str(msg.data + '/answer') # Suffix '/answer' is sent to the client

    print('Websocket connection closed')
    return ws

'''
    The main function inits the asyncio loop,
    handles requests under '/'
    and runs the app.
'''
def main():
    loop = asyncio.get_event_loop()
    app = aiohttp.web.Application(loop=loop)
    app.router.add_route('GET', '/', websocket_handler)
    aiohttp.web.run_app(app, host=HOST, port=PORT)

# Start main()
if __name__ == '__main__':
    main()
