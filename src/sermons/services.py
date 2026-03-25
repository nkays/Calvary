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

def get_sermon_detail(series_id=None, sermon_id=None):
    if sermon_id is None or series_id is None:
        return None
    obj = None
    try:
        obj = Sermon.objects.get(
            youtube_id=sermon_id,
            series__slug=series_id
        )
    except Sermon.DoesNotExist:
        return None
    return obj
    

    
def get_published_sermons():
    return Sermon.objects.filter(status="published")


