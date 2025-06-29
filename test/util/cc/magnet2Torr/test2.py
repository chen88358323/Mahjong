import asyncio
from torrentp import TorrentDownloader
torrent_file = TorrentDownloader("magnet:...", '.')
# Start the download process
asyncio.run(torrent_file.start_download()) # start_download() is a asynchronous method

# Pausing the download
torrent_file.pause_download()

# Resuming the download
torrent_file.resume_download()

# Stopping the download
torrent_file.stop_download()