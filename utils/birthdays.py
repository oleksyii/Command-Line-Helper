from datetime import datetime


def string_to_date(date_string) -> datetime:
    "Converts a string with a format '%Y.%m.%d' into a datetime object. The opposite for date_to_string()"
    return datetime.strptime(date_string, "%Y.%m.%d").date()


def date_to_string(date: datetime) -> str:
    "Converts a datetime object into a string with a format '%Y.%m.%d'. The opposite for string_to_date()"
    return date.strftime("%Y.%m.%d")
