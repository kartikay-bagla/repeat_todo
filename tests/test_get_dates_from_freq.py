from datetime import datetime, timedelta

import pandas as pd

from repeat_todo.utils import get_dates_from_freq


def test_get_dates_from_freq_daily():
    """
    Test that get_dates_from_freq returns the correct dates for daily
    frequency.
    """
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = today + timedelta(days=5)

    dates = get_dates_from_freq("DAILY", end_date)
    date_range = pd.date_range(today, end_date)

    assert (dates == date_range).all()


def test_get_dates_from_freq_weekly():
    """
    Test that get_dates_from_freq returns the correct dates for weekly
    frequency.
    """
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = today + timedelta(days=20)

    dates = get_dates_from_freq("WEEKLY", end_date)
    date_range = pd.date_range(today, end_date, freq="W")

    assert (dates == date_range).all()


def test_get_dates_from_freq_monthly():
    """
    Test that get_dates_from_freq returns the correct dates for monthly
    frequency.
    """
    today = datetime.now().replace(
        day=1, hour=0, minute=0, second=0, microsecond=0
    )
    end_date = today + timedelta(days=35)

    dates = get_dates_from_freq("MONTHLY", end_date)
    date_range = pd.date_range(today, end_date, freq="M")

    assert (dates == date_range).all()
