# youtube.py/clean-final-version
from googleapiclient.discovery import build
from decouple import config
from sermons.models import Sermon, Series
from django.utils.dateparse import parse_datetime


def get_youtube_client():
    return build("youtube", "v3", developerKey=config("YOUTUBE_API_KEY"))


# youtube.py/normalize_video_data/helper
def normalize_video_data(item):
    snippet = item.get("snippet", {})
    resource = snippet.get("resourceId", {})

    return {
        "title": snippet.get("title"),
        "youtube_id": resource.get("videoId"),
        "description": snippet.get("description"),
        "published_at": snippet.get("publishedAt"),


    }


# youtube.py/get_playlist_videos/core-fetch
def get_playlist_videos(playlist_id, max_results=50):
    youtube = get_youtube_client()

    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=max_results
    )

    response = request.execute()

    videos = []

    for item in response.get("items", []):
        video_data = normalize_video_data(item)

        if not video_data["youtube_id"]:
            continue

        videos.append(video_data)

    return videos


# youtube.py/sync_playlist_to_series/core-sync
def sync_playlist_to_series(series: Series):
    if not isinstance(series, Series):
        raise ValueError("A valid Series instance is required")

    if not series.youtube_playlist_id:
        return {"created": [], "updated": []}

    videos = get_playlist_videos(series.youtube_playlist_id)

    created = []
    updated = []

    for video in videos:
        obj, was_created = Sermon.objects.update_or_create(
            youtube_id=video["youtube_id"],
            defaults={
                "title": video["title"],
                "description": video["description"],
                "published_at": parse_datetime(video["published_at"]) 
                    if video["published_at"] else None,
                "series": series,
                "status": "published",
            }
        )

        if was_created:
            created.append(obj)
        else:
            updated.append(obj)

    return {
        "created": created,
        "updated": updated,
    }

# youtube.py/get_channel_playlists/fetch-playlists
def get_channel_playlists(channel_id, max_results=200):
    youtube = get_youtube_client()

    request = youtube.playlists().list(
        part="snippet",
        channelId=channel_id,
        maxResults=max_results
    )

    response = request.execute()

    playlists = []

    for item in response.get("items", []):
        snippet = item.get("snippet", {})

        playlists.append({
            "title": snippet.get("title"),
            "description": snippet.get("description"),
            "playlist_id": item.get("id"),
        })

    return playlists

# youtube.py/sync_channel_to_series/core-sync
def sync_channel_to_series(channel_id):
    if not channel_id:
        raise ValueError("A valid channel_id is required")

    playlists = get_channel_playlists(channel_id)

    created = []
    updated = []

    for playlist in playlists:
        obj, was_created = Series.objects.update_or_create(
            youtube_playlist_id=playlist["playlist_id"],
            defaults={
                "title": playlist["title"],
                "description": playlist["description"],
            }
        )

        if was_created:
            created.append(obj)
        else:
            updated.append(obj)

    return {
        "created": created,
        "updated": updated,
    }

# youtube.py/get_channel_id_from_handle/helper
def get_channel_id_from_handle(handle):
    youtube = get_youtube_client()

    request = youtube.search().list(
        part="snippet",
        q=handle,
        type="channel",
        maxResults=1
    )

    response = request.execute()
    items = response.get("items", [])

    if not items:
        return None

    return items[0]["snippet"]["channelId"]

# youtube.py/full_sync_channel/orchestrator
from sermons.models import Series




# youtube.py/get_uploads_playlist_id/helper
def get_uploads_playlist_id(channel_id):
    youtube = get_youtube_client()

    request = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    )

    response = request.execute()
    items = response.get("items", [])

    if not items:
        return None

    return items[0]["contentDetails"]["relatedPlaylists"]["uploads"]

# youtube.py/sync_uploads_to_sermons/core-sync
def sync_uploads_to_sermons(channel_id):
    uploads_playlist_id = get_uploads_playlist_id(channel_id)

    if not uploads_playlist_id:
        return {"created": [], "updated": []}

    standalone_series, _ = Series.objects.get_or_create(
        title="Standalone Sermons",
        defaults={"description": "Sermons not part of a series"}
    )

    videos = get_playlist_videos(uploads_playlist_id)

    created = []
    updated = []

    for video in videos:
        obj, was_created = Sermon.objects.update_or_create(
            youtube_id=video["youtube_id"],
            defaults={
                "title": video["title"],
                "description": video["description"],
                "published_at": parse_datetime(video["published_at"]) if video["published_at"] else None,
                # 🚫 DO NOT set series here
                "status": "published",
            }
        )

        # ✅ ONLY assign series if NEW
        if was_created:
            obj.series = standalone_series
            obj.save()
            created.append(obj)
        else:
            updated.append(obj)

    return {
        "created": created,
        "updated": updated,
    }

def full_sync_channel(channel_id):
    if not channel_id:
        raise ValueError("A valid channel_id is required")

    # Step 1: Sync playlists → Series
    series_result = sync_channel_to_series(channel_id)

    # Step 2: Sync each Series → Sermons
    sermon_created_total = 0
    sermon_updated_total = 0

    for series in Series.objects.exclude(youtube_playlist_id__isnull=True):
        result = sync_playlist_to_series(series)

        sermon_created_total += len(result["created"])
        sermon_updated_total += len(result["updated"])
    
    # 3. 🔥 Sync uploads (non-playlist videos)
    uploads_result = sync_uploads_to_sermons(channel_id)

    return {
        "series_created": len(series_result["created"]),
        "series_updated": len(series_result["updated"]),
        "sermons_created": sermon_created_total + len(uploads_result["created"]),
        "sermons_updated": sermon_updated_total + len(uploads_result["updated"]),
    }