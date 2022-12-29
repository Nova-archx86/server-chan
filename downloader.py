import os
import logging
from discord import Embed, Color
from yt_dlp import YoutubeDL

class Downloader:

    def __init__(self, url):
        
        self.url = url
        self.options = {
            'format': 'bestaudio',
            'outtmpl': '%(title)s',
            'quiet': True,
            'noplaylist': True,
            'source_address': '0.0.0.0'
        }
    
    @staticmethod
    def create_embed(name, info) -> Embed:
        title, duration, thumbnail, author = info
        em = Embed(title=name, color=Color.random())
        em.set_thumbnail(url=thumbnail)
        em.add_field(name='Song', value=title, inline=False)
        em.add_field(name='Channel', value=author, inline=False)
        em.add_field(name='Duration', value=duration, inline=False)
        
        return em


    def get_info(self) -> tuple:
        video_info = None

        with YoutubeDL(self.options) as yt: 
            info = yt.extract_info(self.url, download=False)
            title = info.get('title')
            author = info.get('uploader')
            thumbnail = info.get('thumbnail')
            
            # Formats duration in mm:ss 
            duration_secs = info.get('duration')
            mins, secs = divmod(duration_secs, 60)
            duration = f'{mins}:{secs}'
            video_info = (title, duration, thumbnail, author)

            return video_info

    def download(self):
        with YoutubeDL(self.options) as yt:
            os.chdir('./music') 
            yt.download([self.url])
            os.chdir('../')

