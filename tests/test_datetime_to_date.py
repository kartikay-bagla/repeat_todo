from datetime import datetime

from repeat_todo.utils import datetime_to_date


def test_datetime_to_date():
    """
    Test that datetime_to_date returns the correct date.
    """
    date = datetime(2020, 1, 1, 0, 0, 0)
    assert datetime_to_date(date) == date

    date = datetime(2020, 1, 5, 23, 59, 59)
    assert datetime_to_date(date) == datetime(2020, 1, 5, 23)
    assert datetime_to_date(date, hour=False) == datetime(2020, 1, 5)
