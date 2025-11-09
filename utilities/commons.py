import datetime


def get_formatted_date(date_obj):
    """
    Formats a datetime object to 'YYYY-MM-DD' string format.
    Args:
        date_obj (datetime): The datetime object to format.
    Returns:
        str: Formatted date string.
    """
    return date_obj.strftime('%Y-%m-%d').date()

