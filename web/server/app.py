import asyncio
import os

import aiohttp.web, json
from web.server.ydl.downloader import DownloaderAPI

# Bind to 0.0.0.0:8080
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 8080))

''' websocket_handler(request)
        Handles all requests under '/'
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

            try: # Deserialize data & check if it a request to predict
                data_dict = json.loads(msg.data)
                print(data_dict)

                request = data_dict.get('request_type')

                if (request == "predict"):

                    print("Call predict method here")
                    pass # predict
            except: # If not a request to predict
                print("This is not a request for the server to predict")
                pass

            # Init DownloaderAPI Class in order to check & download song
            song = DownloaderAPI(msg.data)

            try:
                song.urlValidation()
                await ws.send_str("Your video is valid!")

                song.download()
                await ws.send_str("URL downloading completed!")
            except:
                await ws.send_str("Bad URL")

            if msg.data == 'close': # If client sends 'close', websocket closes
                await ws.close()
                print('Websocket connection closed')
    return ws

''' index_handler(request):
        Serves the `index.html` file
'''
async def index_handler(request):
    return aiohttp.web.FileResponse('web/server/static/index.html')

''' main()
        Inits the asyncio loop,
        handles requests under '/'
        and runs the app.
'''
def main():
    path_to_static_folder = os.getcwd() + '/web/server/static/'

    loop = asyncio.get_event_loop()
    app = aiohttp.web.Application(loop=loop)
    app.router.add_route('GET', '/ws', websocket_handler)
    app.router.add_route('GET', '/', index_handler)
    app.router.add_static('/server/static', path_to_static_folder, name='static')
    aiohttp.web.run_app(app, host=HOST, port=PORT)


# Start main()
if __name__ == '__main__':
    main()
