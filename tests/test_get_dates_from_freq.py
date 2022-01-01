from datetime import datetime, timedelta

import pandas as pd

from repeat_todo.utils import datetime_to_date, get_dates_from_freq


def test_get_dates_from_freq_daily():
    """
    Test that get_dates_from_freq returns the correct dates for daily
    frequency.
    """
    today = datetime_to_date(datetime.now(), hour=False)
    end_date = today + timedelta(days=5)

    dates = get_dates_from_freq("DAILY", end_date)
    date_range = pd.date_range(today, end_date)

    assert (dates == date_range).all()

    today = datetime(2020, 1, 1, 0, 0, 0)
    end_date = datetime(2020, 1, 5, 0, 0, 0)

    dates = get_dates_from_freq("DAILY", end_date, start_date=today)
    date_range = pd.date_range(today, end_date)

    assert (dates == date_range).all()


def test_get_dates_from_freq_weekly():
    """
    Test that get_dates_from_freq returns the correct dates for weekly
    frequency.
    """
    today = datetime_to_date(datetime.now(), hour=False)
    end_date = today + timedelta(days=20)

    dates = get_dates_from_freq("WEEKLY", end_date)
    date_range = pd.date_range(today, end_date, freq="W")

    assert (dates == date_range).all()

    today = datetime(2020, 1, 1, 0, 0, 0)
    end_date = datetime(2020, 1, 20, 0, 0, 0)

    dates = get_dates_from_freq("WEEKLY", end_date, start_date=today)
    date_range = pd.date_range(today, end_date, freq="W")

    assert (dates == date_range).all()


def test_get_dates_from_freq_monthly():
    """
    Test that get_dates_from_freq returns the correct dates for monthly
    frequency.
    """
    today = datetime_to_date(datetime.now(), hour=False)
    end_date = today + timedelta(days=35)

    dates = get_dates_from_freq("MONTHLY", end_date)
    date_range = pd.date_range(today, end_date, freq="M")

    assert (dates == date_range).all()

    today = datetime(2020, 1, 1, 0, 0, 0)
    end_date = datetime(2020, 3, 20, 0, 0, 0)

    dates = get_dates_from_freq("MONTHLY", end_date, start_date=today)
    date_range = pd.date_range(today, end_date, freq="M")

    assert (dates == date_range).all()
