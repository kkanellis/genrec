import asyncio
import json
import os

import aiohttp.web
import aiohttp_jinja2
import jinja2

from web.api import GenrecAPI
from web.server.ydl.downloader import DownloaderAPI

# Bind to 0.0.0.0:8080
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 8080))

genrec_api = GenrecAPI()
classifiers = genrec_api.get_available_classifiers('gtzan')['gtzan']['classifiers'] # FIXME

yt_api = DownloaderAPI()

def make_reply(req_type, msg, success=True):
    return json.dumps({
        'command' : req_type[:-3] + "REP",
        'success' : success,
        'message': msg,
    })

async def websocket_handler(request):
    """
    Handles all requests under '/'
    Also, it prints all messages that gets from the client
    If message is 'close', the websocket closes.
    """
    print('Websocket connection starting')
    ws = aiohttp.web.WebSocketResponse() # Creates websocket in request

    await ws.prepare(request)
    print('Websocket connection ready')

    # incoming message loop
    async for msg in ws:
        if msg.type != aiohttp.WSMsgType.TEXT:
            print('ERROR: Invalid message type')
            continue

        try:
            request = json.loads(msg.data)
            print(request)

            command  = request.get('command')
            if command == "VALIDATE_URL_REQ":
                url = request.get('url')
                videoId = yt_api.is_url_valid(url)
                if videoId:
                    await ws.send_str(
                        make_reply(command, "Url is valid. Will start download!")
                    )
                    yt_api.download(videoId, url)
                else:
                    await ws.send_str(
                        make_reply(command, "Invalid youtube URL!", success=False)
                    )
            elif command == "PREDICT_REQ":
                print("Prediction request")

                videoId = request.get('videoId')
                classifier = request.get('classifier')
                dataset = request.get('dataset')

                print(videoId, classifier, dataset)

                filepath = yt_api.get_filepath(videoId)
                prediction_json = genrec_api.predict_song(filepath, dataset, classifier)
                prediction_json.update({
                    'command': 'PREDICT_REP',
                    'success': True,
                })

                await ws.send_str(
                    json.dumps(prediction_json)
                )

        except Exception as ex:
            print(f"ERROR: {ex.msg}")
            await ws.send_str(
                make_reply(NACK, ex.msg)
            )

    return ws

@aiohttp_jinja2.template('index.html')
async def index_handler(request):
    """ Serves the `index.html` file """
    return { 'classifiers': classifiers }

def main():
    """ Inits the asyncio loop, handles requests under '/' and runs the app. """
    path_to_static_folder = os.path.join(os.getcwd(), 'web/server/static/')

    loop = asyncio.get_event_loop()
    app = aiohttp.web.Application(loop=loop)

    aiohttp_jinja2.setup(app,
        loader=jinja2.FileSystemLoader(path_to_static_folder))

    app.router.add_route('GET', '/ws', websocket_handler)
    app.router.add_route('GET', '/', index_handler)
    app.router.add_static('/static', path_to_static_folder, name='static', show_index=True, follow_symlinks=True)

    aiohttp.web.run_app(app, host=HOST, port=PORT)

if __name__ == '__main__':
    main()
