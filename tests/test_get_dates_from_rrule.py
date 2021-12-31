from datetime import datetime, timedelta

import pandas as pd

from repeat_todo.utils import get_dates_from_rrule


def test_get_dates_from_rrule_hourly():
    rule = "FREQ=HOURLY"

    today = datetime.now().replace(minute=0, second=0, microsecond=0)
    end_date = today + timedelta(days=5)

    dates = get_dates_from_rrule(rule, end_date)
    date_range = pd.date_range(today, end_date, freq="H")

    assert (dates == date_range).all()


def test_get_dates_from_rrule_daily():
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = today + timedelta(days=5)

    rule = "FREQ=DAILY"

    dates = get_dates_from_rrule(rule, end_date)
    date_range = pd.date_range(today, end_date, freq="D")

    assert (dates == date_range).all()

    today = datetime.now().replace(minute=0, second=0, microsecond=0)
    end_date = today + timedelta(days=5)

    rule = "FREQ=DAILY;BYHOUR=0,12"

    dates = get_dates_from_rrule(rule, end_date)
    date_range = pd.date_range(today, end_date, freq="H")
    date_range = date_range[date_range.hour.isin([0, 12])]

    assert (dates == date_range).all()


def test_get_dates_from_rrule_weekly():
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = today + timedelta(days=10)

    rule = "FREQ=WEEKLY"

    dates = get_dates_from_rrule(rule, end_date)
    date_range = pd.date_range(today, end_date, freq="W")

    assert (dates == date_range).all()

    rule = "FREQ=WEEKLY;BYDAY=MO,WE,FR,SU"

    dates = get_dates_from_rrule(rule, end_date)
    date_range = pd.date_range(today, end_date, freq="D")
    date_range = date_range[date_range.weekday.isin([0, 2, 4, 6])]

    assert (dates == date_range).all()

    rule = "FREQ=WEEKLY;BYDAY=TU,TH,SA"

    dates = get_dates_from_rrule(rule, end_date)
    date_range = pd.date_range(today, end_date, freq="D")
    date_range = date_range[date_range.weekday.isin([1, 3, 5])]

    assert (dates == date_range).all()


def test_get_dates_from_rrule_monthly():
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = today + timedelta(days=35)

    rule = "FREQ=MONTHLY"

    dates = get_dates_from_rrule(rule, end_date)
    date_range = pd.date_range(today, end_date, freq="M")

    assert (dates == date_range).all()

    rule = "FREQ=MONTHLY;BYMONTHDAY=1,15"

    dates = get_dates_from_rrule(rule, end_date)
    date_range = pd.date_range(today, end_date, freq="D")
    date_range = date_range[date_range.day.isin([1, 15])]

    assert (dates == date_range).all()
