# youtube.py/clean-final-version
from googleapiclient.discovery import build
from decouple import config
from sermons.models import Sermon, Series, get_standalone_series
from django.utils.dateparse import parse_datetime


def get_youtube_client():
    return build("youtube", "v3", developerKey=config("YOUTUBE_API_KEY"))


# src/sermons/youtube.py/normalize_video_data/helper
def normalize_video_data(item):
    snippet = item.get("snippet", {})

    video_id = None

    # Primary: playlistItems structure
    resource = snippet.get("resourceId")
    if resource:
        video_id = resource.get("videoId")

    # Fallback (defensive)
    if not video_id:
        video_id = snippet.get("videoId")

    return {
        "title": snippet.get("title"),
        "youtube_id": video_id,
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

    standalone_series = get_standalone_series()
    videos = get_playlist_videos(uploads_playlist_id)

    created = []
    updated = []

    # src/sermons/youtube.py/sync_uploads_to_sermons/core-sync
    for video in videos:
        obj, was_created = Sermon.objects.update_or_create(
            youtube_id=video["youtube_id"],
            defaults={
                "title": video["title"],
                "description": video["description"],
                "published_at": parse_datetime(video["published_at"]) 
                    if video["published_at"] else None,
                "status": "published",
                "series": standalone_series,
            }
        )

        # ✅ ONLY assign series if NEW
        if was_created:
            created.append(obj)
        else:
            updated.append(obj)

    return {
        "created": created,
        "updated": updated,
    }
# src/sermons/youtube.py/collect_video_map
def collect_video_map(channel_id):
    """
    Returns:
        {
            youtube_id: {
                "title": ...,
                "description": ...,
                "published_at": ...,
                "series": Series instance
            }
        }
    """
    video_map = {}

    # 🔹 1. Get standalone series
    standalone_series = get_standalone_series()

    # 🔹 2. Get uploads playlist
    uploads_playlist_id = get_uploads_playlist_id(channel_id)

    if uploads_playlist_id:
        uploads = get_playlist_videos(uploads_playlist_id)

        for video in uploads:
            video_map[video["youtube_id"]] = {
                **video,
                "series": standalone_series
            }

    # 🔹 3. Get all Series (playlists)
    for series in Series.objects.exclude(youtube_playlist_id__isnull=True):
        videos = get_playlist_videos(series.youtube_playlist_id)

        for video in videos:
            # 🔥 Playlist overrides uploads
            video_map[video["youtube_id"]] = {
                **video,
                "series": series
            }

    return video_map

# src/sermons/youtube.py/ingest_videos
def ingest_videos(video_map):
    created = []
    updated = []

    for youtube_id, video in video_map.items():
        obj, was_created = Sermon.objects.update_or_create(
            youtube_id=youtube_id,
            defaults={
                "title": video["title"],
                "description": video["description"],
                "published_at": parse_datetime(video["published_at"]) 
                    if video["published_at"] else None,
                "series": video["series"],
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

# src/sermons/youtube.py/full_sync_channel/orchestrator
def full_sync_channel(channel_id):
    if not channel_id:
        raise ValueError("A valid channel_id is required")

    # 🔹 1. Sync playlists → Series
    series_result = sync_channel_to_series(channel_id)

    # 🔹 2. Collect ALL videos (uploads + playlists)
    video_map = collect_video_map(channel_id)

    # 🔹 3. Ingest once
    result = ingest_videos(video_map)

    return {
        "series_created": len(series_result["created"]),
        "series_updated": len(series_result["updated"]),
        "sermons_created": len(result["created"]),
        "sermons_updated": len(result["updated"]),
    }