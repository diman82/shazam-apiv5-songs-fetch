import asyncio
from aiohttp.client import ClientSession
import codecs, logging, logging.config, os, yaml, json
import re

ROOT_PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(ROOT_PROJECT_DIR, 'logging_config.yaml'), 'r') as f:
    log_cfg = yaml.safe_load(f.read())
logging.config.dictConfig(log_cfg)
logger = logging.getLogger('dev')
logger.setLevel(logging.INFO)


async def main(urls):
    Utf8Decoder = codecs.getincrementaldecoder('utf-8')
    decoder = Utf8Decoder()

    async def resolve_redirect_url(song):
        if 'youtube_uri' in song.keys():
            async with ClientSession() as session:
                r = await session.get(url=song['youtube_uri'][0])
                corrected_song = song

                stream = r.content
                data = await stream.read()
                html = decoder.decode(data)
                m = re.search(r'contents":\[{"videoRenderer":{"videoId":"([a-zA-Z0-9_]{11})",', html)
                if m is not None:
                    corrected_song['youtube_uri'] = "https://www.youtube.com/watch?v=" + m.group(1)
                else:
                    corrected_song['youtube_uri'] = ''
                return corrected_song
        else:
            return song

    async def coro(url):
        async with ClientSession() as session:
            resp = await session.get(url=url)
            if not resp.status == 200:
                logging.error('bad response, response status code is: , ', resp.status)
            stream = resp.content
            data = await stream.read()
            decoded_data = decoder.decode(data)
            return decoded_data

    ops = [coro(url) for url in urls]
    responses = await asyncio.gather(*ops)

    # extract only interesting fields
    songs = []
    for response in responses:
        song_json = json.loads(response)
        if 'title' not in song_json.keys():
            continue  # filter out erroneous rows
        new_song = {'title': song_json['title'],
                    'artist': song_json['subtitle'],
                    'fullname': song_json['share']['subject'],
                    'spotify_uri': song_json['hub']['providers'][0]['actions'][0]['uri'] if 'providers' in song_json[
                        'hub'].keys() else False,
                    'shazam_uri': song_json['url'],
                    'youtube_uri': [section['actions'][0]['uri'] for section in song_json['sections']
                                    if
                                    (section['type'] == 'VIDEO' and 'actions' in section.keys())]}  # synchronous fetch
        songs.append(new_song)

    ops2 = [resolve_redirect_url(song) for song in songs]
    songs_with_youtube_links = await asyncio.gather(*ops2)

    with open('songs.json', 'w') as txtfile:
        json.dump(songs, txtfile)

    print('All finished')


if __name__ == '__main__':
    urls = list(open('urls.txt'))
    asyncio.run(main(urls), debug=True)
