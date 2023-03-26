import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
#GOAL: When artist I follow uploads new song/album add to playlist


def handler(event, context):
    main()
    return
    
def getNewReleases(sp):
    map = {}
    response = sp.new_releases()
    while response:
        albums = response['albums']
        for i, item in enumerate(albums['items']):
            map[item['artists'][0]['name']] = item['uri']
        if albums['next']:
            response = sp.next(albums)
        else:
            response = None
    return map
def main():
    #authManager = SpotifyClientCredentials()
    scope = "playlist-modify-public "
    scope += 'user-follow-read'
    createNewPlayList = True
    token = spotipy.util.prompt_for_user_token('rahilkapur', scope=scope)
    sp = spotipy.Spotify(auth=token)
    playId = ''
    releasedMap = getNewReleases(sp)
    followedArtistList = []
    followedArtists = sp.current_user_followed_artists(limit=30)
    for i, item in enumerate(followedArtists['artists']['items']):
        followedArtistList.append(item['name'])
    albumList = []
    for artist in releasedMap:
        if artist in followedArtistList:
            albumList.append(releasedMap[artist])
    trackIDList = []
    for albumuri in albumList:
        for track in sp.album_tracks(albumuri)['items']:
            trackIDList.append(track['uri'])
    if not trackIDList:
        return
    userID = sp.me()['id']
    playlists = sp.user_playlists(userID)
    for playlist in playlists['items']:
        if playlist['name'] == 'updatedPlaylist':
            createNewPlayList = False
            playId = playlist['id']
            
    if createNewPlayList:
        playlist = sp.user_playlist_create(userID, name='updatedPlaylist', description='updated regularly')
        sp.playlist_add_items(playlist_id=playlist['id'], items=trackIDList)
    else:
        sp.playlist_add_items(playId, trackIDList)

