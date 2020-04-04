import datetime


def utcnow():
    """ Return a non-naive UTC datetime object
    """
    return datetime.datetime.now(datetime.timezone.utc)
