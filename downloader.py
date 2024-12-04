import os
from yt_dlp import YoutubeDL

class Downloader:
    def __init__(self, destination_folder):
        self.dest = destination_folder  # Dossier de téléchargement
        self.busy = False
        self.success = True

    def get_formats(self, url):
        """Retourne les formats MP4 disponibles pour une vidéo."""
        options = {'quiet': True, 'extract_flat': True}
        with YoutubeDL(options) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                formats = [
                    {
                        'id': f['format_id'],
                        'size': f.get('filesize', 'N/A'),
                        'resolution': f.get('height', 'N/A'),
                        'format': f.get('format', '-')
                    }
                    for f in info.get('formats', [])
                    if 'mp4' in f.get('ext', '') and f.get('filesize') and 'avc' in f.get('vcodec', '')
                ]
                return {'thumbnail': info.get('thumbnail', ''), 'formats': formats}
            except Exception as e:
                print(f"[ERROR]: {e}")

    def change_dest_folder(self, new_dest):
        """Change le dossier de destination."""
        if os.path.exists(new_dest):
            self.dest = new_dest
        else:
            print(f"[ERROR]: Path «{new_dest}» doesn't exist.")

    def download(self, url, format_id=None, progress_hooks=[]):
        """Télécharge une vidéo YouTube."""
        ydl_opts = {
            "quiet": True,
            'format': (f"{format_id}" or 'bestvideo[height<=720]') + 'bestaudio/best',
            'outtmpl': os.path.join(self.dest, '%(title)s.%(ext)s'),
            'progress_hooks': progress_hooks
        }
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.success = True
        except Exception as e:
            print(f"Download error: {e}")
            self.success = False
