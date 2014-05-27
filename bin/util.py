from time import strptime, mktime
from datetime import date

from logger import LOGGER


def fail(reason="unknown reason"):
    LOGGER.error("Table is inconsistent: %s" % reason)
    exit(1)


def format_date(date_string):
    result = date_string
    try:
        time_struct = strptime(date_string, "%d/%b/%y")
        result = date.fromtimestamp(mktime(time_struct))
    except (TypeError, ValueError):
        LOGGER.warn('[%s] is not valid date' % date_string)
    return result

