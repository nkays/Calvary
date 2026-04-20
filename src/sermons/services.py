# services.py/get_published_sermons/query
from django.db.models import Q
from .models import Sermon, Series, PublishStatus, AccessRequirement

    
def get_series():
    return Series.objects.all()# services.py/get_sermon_detail/query

def get_series_detail(series_id=None):
    if series_id is None:
        return None
    obj = None
    try:
        obj = Series.objects.get(
            slug=series_id,
        )
    except Series.DoesNotExist:
        return None
    return obj
    
# services.py/get_sermons_by_series/query
def get_sermons_by_series(series):
    return series.sermons.filter(access='anyone')

def get_sermon_detail(series_slug=None, youtube_id=None):
    from .models import Sermon

    try:
        return Sermon.objects.select_related("series").get(
            youtube_id=youtube_id,
            series__slug=series_slug
        )
    except Sermon.DoesNotExist:
        return None
    

    
def get_published_sermons():
    return Sermon.objects.filter(status="published")

def get_featured_sermons(limit=None):
    from .models import Sermon, Series

    featured_series = Series.objects.filter(featured=True).first()

    if not featured_series:
        return []

    queryset = Sermon.objects.filter(
        series=featured_series
    ).order_by('-published_at')

    if limit:
        queryset = queryset[:limit]

    return queryset
