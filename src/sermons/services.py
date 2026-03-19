# services.py/get_published_sermons/query
from .models import Sermon


def get_published_sermons():
    return Sermon.objects.filter(status="published")

# services.py/get_sermon_detail/query
def get_sermon_detail(sermon_id=None):
    if sermon_id is None:
        return None
    try:
        return Sermon.objects.get(id=sermon_id, status="published")
    except Sermon.DoesNotExist:
        return None
    
# services.py/get_sermons_by_series/query
def get_sermons_by_series(series):
    return series.sermons.filter(status="published")