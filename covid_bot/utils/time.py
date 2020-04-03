import datetime


def utcnow():
    """ Return a non-naive UTC datetime object
    """
    return datetime.datetime.utcnow(datetime.timezone.utc)
