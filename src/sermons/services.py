# services.py/get_published_sermons/query
from .models import Sermon, Series, PublishStatus, AccessRequirement


def get_published_sermons():
    return Sermon.objects.filter(status="published")


    
# services.py/get_sermons_by_series/query
def get_sermons_by_series(series):
    return series.sermons.filter(status="published")

    
def get_series():
    return Series.objects.all().order_by("-created_at")# services.py/get_sermon_detail/query



def get_sermon_detail(series_id=None, sermon_id=None):
    if sermon_id is None or series_id is None:
        return None
    obj = None
    try:
        return Sermon.objects.get(
            series___id=series_id,
            series___status=PublishStatus.PUBLISHED,
            status=PublishStatus.PUBLISHED,
            id=sermon_id, 
        )
    except Sermon.DoesNotExist:
        return None