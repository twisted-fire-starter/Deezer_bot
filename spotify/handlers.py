import re

from deezer import deezer_api
from deezer import methods as dz_methods
from bot import bot
from var import var

async def spotify_handler(message, track_id):
    spotify_song = await var.spot.get_track(track_id)
    print(track_id)
    search_query = '%s %s' % (
        spotify_song.artists[0].name,
        re.match(r'[^\(\[\-]+', spotify_song.name).group(0))
    search_results = await deezer_api.search(q=search_query)
    if not search_results:
        return await bot.send_message(
            message.chat.id, 'Sorry, track is not found on Deezer')
    print(search_results[0])
    await dz_methods.send_track(search_results[0], message.chat)


async def spotify_playlist_handler(message, playlist_id):
    spotify_playlist = await var.spot.get_playlist(playlist_id)
    for track in spotify_playlist:  
        try:
            search_query = '{} {}'.format(
                track.artists[0].name, re.match(r'[^\(\[\-]+', track.name).group(0))
            search_results = await deezer_api.search(q=search_query)
            if search_results:
                await dz_methods.send_track(search_results[0], message.chat)
            else:
                await bot.send_message(
                    chat_id=message.chat.id,
                    text=f'Sorry, track {track.artists[0].name} - {track.name} is not found on Deezer')
        except Exception as e:
            print(e)
        await sleep(.5)


async def spotify_album_handler(message, album_id):
    spotify_album = await var.spot.get_album(album_id)
    search_results = await deezer_api.search(
        'album', f'{spotify_album.artists[0].name} {spotify_album.name}')
    if not search_results:
        return await bot.send_message(
            chat_id=message.chat.id,
            text=f'Sorry, album {spotify_album.name} by {spotify_album.artists[0].name} is not found on Deezer')
    await dz_methods.send_album(search_results[0], message.chat)


async def spotify_artist_handler(message, artist_id):
    spotify_artist = await var.spot.get_artist(artist_id)
    search_results = await deezer_api.search('artist', spotify_artist.name)
    await dz_methods.send_artist(search_results[0], message.chat.id)