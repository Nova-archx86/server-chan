import os
from yt_dlp import YoutubeDL

class Downloader:

    def __init__(self, url):
        
        self.url = url
        
        # the output filename is the video id due to some 
        # youtube video titles having names that don't play nice
        # with bash or any shell for that matter

        self.options = {
            'format': 'bestaudio',
            'outtmpl': '%(id)s',
            'quiet': True,
            'noplaylist': True,
            'source_address': '0.0.0.0'
        }
    
    def get_info(self) -> tuple:
        video_info = None

        with YoutubeDL(self.options) as yt: 
            info = yt.extract_info(self.url, download=False)
            
            id = info.get('id') 
            title = info.get('title')
            author = info.get('uploader')
            thumbnail = info.get('thumbnail')
            
            # Formats duration in mm:ss 
            duration_secs = info.get('duration')
            mins, secs = divmod(duration_secs, 60)
            duration = f'{mins}:{secs}'
            video_info = (id, title, duration, thumbnail, author)

            return video_info

    def download(self):
        with YoutubeDL(self.options) as yt:
            os.chdir('./music') 
            yt.download([self.url])
            os.chdir('../')

