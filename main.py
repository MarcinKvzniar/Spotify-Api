"""
This is a simple script that uses the Spotify API
to search for an artist and then get their top tracks.
Source: "https://www.youtube.com/watch?v=WAmEZBEeNmg"
"""


import json
import os
import base64
from dotenv import load_dotenv
from requests import post, get


load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


def get_token():
    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]

    return token


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


def search_for_artist(artist_name, token):
    url = f"https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    query_url = url + query

    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]

    if len(json_result) == 0:
        print("No artist found")
        return None
    else:
        print(f"Found artist: {json_result[0]['name']}")
        print(f"Artist ID: {json_result[0]['id']}")
        print(f"Artist URL: {json_result[0]['external_urls']['spotify']}")
        print(f"Artist Popularity: {json_result[0]['popularity']}")
        print(f"Artist Genres: {json_result[0]['genres']}")
        print(f"Artist Followers: {json_result[0]['followers']['total']}")

        return json_result[0]


def get_songs_for_artist(artist_id, token):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=PL"
    headers = get_auth_header(token)

    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]

    return json_result


token = get_token()

artist_name = input("Enter artist name: ")

result = search_for_artist(artist_name, token)
artist_id = result["id"]
songs = get_songs_for_artist(artist_id, token)

print("\nTop tracks:")
for idx, song in enumerate(songs):
    print(f"{idx + 1}. {song['name']}")
