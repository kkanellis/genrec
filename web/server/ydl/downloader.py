from __future__ import unicode_literals
import youtube_dl


class DownloaderAPI():

    def __init__(self, url):
        self.ydl_opts = { # options for youtube_dl
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'downloads/%(title)s.%(ext)s'
        }

        # youtube link
        self.url = url

        # initiliaze the ydlObject
        self.ydl = youtube_dl.YoutubeDL(self.ydl_opts)


    def urlValidation(self):
        try:
            # Get information about the YouTube video/song
            info_dict = self.ydl.extract_info(self.url, download=False)

        except: # The url does not exists or is wrong!
            raise 

    def download(self):
        try:
            self.ydl.download([self.url])

        except: # something went wrong at downloading process!
            raise
