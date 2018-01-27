from __future__ import unicode_literals
import os
import os.path

import youtube_dl

class DownloaderAPI():
    DOWNLOAD_LOCATION = 'downloads/'
    available_videos = { }

    def __init__(self):
        self.ydl_opts = { # options for youtube_dl
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': self.DOWNLOAD_LOCATION + '%(id)s.%(ext)s'
        }

        # initiliaze the ydlObject
        self.ydl = youtube_dl.YoutubeDL(self.ydl_opts)
        self._populate_entries()

    def is_url_valid(self, url):
        try:
            # Get information about the YouTube video/song
            info = self.ydl.extract_info(url, download=False)
            return info['id']
        except:
            # The url does not exists or is wrong!
            return None

    def download(self, videoId, url):
        if videoId not in self.available_videos:
            try:
                self.ydl.download([url])
            except: # something went wrong at downloading process!
                raise

            filepath = os.path.join( self.DOWNLOAD_LOCATION, videoId + '.mp3' )
            self.available_videos[videoId] = filepath

            print(f'Saved video "{videoId}" @ "{filepath}"')
        else:
            print(f'Video "{videoId}" already downloaded!')

    def get_filepath(self, videoId):
        return self.available_videos[videoId]

    def _populate_entries(self):
        entries = { }
        for p in os.scandir(self.DOWNLOAD_LOCATION):
            if p.is_file():
                videoId = p.name.split('.')[0]
                entries[videoId] = os.path.realpath(p.path)

        self.available_videos = entries
