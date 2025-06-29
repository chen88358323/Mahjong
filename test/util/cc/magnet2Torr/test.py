import asyncio

from magnet2torrent import Magnet2Torrent, FailedToFetchException

async def fetch_that_torrent():
    # m2t = Magnet2Torrent("magnet:?xt=urn:btih:e2467cbf021192c241367b892230dc1e05c0580e&dn=ubuntu-19.10-desktop-amd64.iso&tr=https%3A%2F%2Ftorrent.ubuntu.com%2Fannounce&tr=https%3A%2F%2Fipv6.torrent.ubuntu.com%2Fannounce")
    m2t = Magnet2Torrent(
        "magnet:?xt=urn:btih:480643b95842abbcb2fb9c07db8e3004512b9d0a")

    try:
        filename, torrent_data = await m2t.retrieve_torrent()
    except FailedToFetchException:
        print("Failed")


if __name__ == '__main__':
    asyncio.run(fetch_that_torrent())