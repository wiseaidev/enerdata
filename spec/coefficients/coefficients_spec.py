# -*- coding: utf-8 -*-
from datetime import datetime
from dateutil.relativedelta import relativedelta
from enerdata.profiles.profile import REEProfile, Profile
from enerdata.contracts.tariff import T20A, T20TD
from enerdata.datetime.timezone import TIMEZONE
from mamba import description, it, before, context
import logging

logger = logging.getLogger(__name__)


ONE_MONTH_DATE_SET = ['1/2018']
DATE_SET = ['3/2018', '4/2018', '5/2018']


class FakeClass(object):
    @classmethod
    def get_range(cls, start, end):
        cofs = []
        start = datetime(start.year, start.month, 1)
        end = datetime(end.year, end.month, 1)
        while start <= end:
            logger.debug('Downloading coefficients for {0}/{1}'.format(
                start.month, start.year
            ))
            cofs.extend(REEProfile.get(start.year, start.month))
            start += relativedelta(months=1)
        return cofs


def get_data_ranges(start, end):
    cofs = []
    start = datetime(start.year, start.month, 1)
    end = datetime(end.year, end.month, 1)
    while start <= end:
        cof = '{0}/{1}'.format(start.month, start.year)
        cofs.append(cof)
        start += relativedelta(months=1)
    return cofs


def first_day_of_month(end):
    return end.day == 1 and end.hour > 0


with description('Downloading coefficients fully months'):
    with it("mustn't include the final month"):
        coeff = REEProfile.get_range(
            datetime(2018, 3, 24, 0, 0),
            datetime(2018, 5, 1, 0, 0) - relativedelta(days=1)
        )
        assert coeff[-1].hour.month == 5

    with it('must include final date end of month'):
        di = datetime(2018, 3, 24, 0, 0)
        df = datetime(2018, 6, 1, 0, 0)
        if first_day_of_month(df):
            assert get_data_ranges(di, df) == DATE_SET
        else:
            assert get_data_ranges(di, df - relativedelta(days=1)) == DATE_SET

    with it('must include final date start of month'):
        di = datetime(2018, 3, 24, 0, 0)
        df = datetime(2018, 5, 1, 1, 0)
        if first_day_of_month(df):
            assert get_data_ranges(di, df) == DATE_SET
        else:
            assert get_data_ranges(di, df - relativedelta(days=1)) == DATE_SET

    with it('must include final date between month'):
        di = datetime(2018, 3, 24, 0, 0)
        df = datetime(2018, 5, 15, 0, 0)
        if first_day_of_month(df):
            assert get_data_ranges(di, df) == DATE_SET
        else:
            assert get_data_ranges(di, df - relativedelta(days=1)) == DATE_SET

    with it('must include one month invoice'):
        di = datetime(2018, 1, 1, 1, 0)
        df = datetime(2018, 2, 1, 0, 0)
        if first_day_of_month(df):
            assert get_data_ranges(di, df) == ONE_MONTH_DATE_SET
        else:
            assert get_data_ranges(
                di, df - relativedelta(days=1)) == ONE_MONTH_DATE_SET

    with it('must include one day invoice'):
        di = datetime(2018, 1, 1, 1, 0)
        df = datetime(2018, 1, 2, 0, 0)
        if first_day_of_month(df):
            assert get_data_ranges(di, df) == ONE_MONTH_DATE_SET
        else:
            assert get_data_ranges(
                di, df - relativedelta(days=1)) == ONE_MONTH_DATE_SET

with description('When profiling'):
    with before.all:
        # Check that the get_coefs changes do not break the profiling"
        self.measures = []
        self.expected_hours = 744

    with context("a full month"):
        with it("must profile the number of hours of the month"):
            start = TIMEZONE.localize(datetime(2018, 5, 1, 1))
            end = TIMEZONE.localize(datetime(2018, 6, 1, 0))
            tariff = T20A()
            accumulated = 0
            balance = {
                'P1': 6.8,
                'P2': 3,
                'P3': 3.5,
            }

            profile = Profile(start, end, self.measures, accumulated)
            estimation = profile.estimate(tariff, balance)

            assert self.expected_hours == len(estimation.measures)
            assert start == estimation.start_date
            assert end == estimation.end_date

    with context("with first day of month included"):
        with it("must return until the last hour of first day of the month"):
            start = TIMEZONE.localize(datetime(2018, 1, 1, 1))
            end = TIMEZONE.localize(datetime(2018, 2, 1, 1))
            tariff = T20A()
            accumulated = 0
            balance = {
                'P1': 6.8,
                'P2': 3,
                'P3': 3.5,
            }

            profile = Profile(start, end, self.measures, accumulated)
            estimation = profile.estimate(tariff, balance)

            assert self.expected_hours + 1 == len(estimation.measures)
            assert start == estimation.start_date
            assert end == estimation.end_date

    with context("with current date to download REE coefficients last month"):
        with it("must throw the exception of: Profiles from REE not found"):
            end_year = datetime.now().year
            end_month = datetime.now().month
            start = TIMEZONE.localize(datetime(2022, 6, 1, 1))
            end = TIMEZONE.localize(datetime(end_year, end_month, 1, 0))

            tariff = T20TD()
            accumulated = 0
            balance = {
                'P1': 6.8,
                'P2': 3,
                'P3': 3.5,
            }

            profile = Profile(start, end, self.measures, accumulated)
            try:
                estimation = profile.estimate(tariff, balance)
            except Exception as err:
                assert err.message == "Profiles from REE not found"

    with context("not habitual hours"):
        with it("must profile up to specific times"):
            start = TIMEZONE.localize(datetime(2018, 1, 1, 5))
            end = TIMEZONE.localize(datetime(2018, 2, 1, 11))
            tariff = T20A()
            accumulated = 0
            balance = {
                'P1': 6.8,
                'P2': 3,
                'P3': 3.5,
            }

            profile = Profile(start, end, self.measures, accumulated)
            estimation = profile.estimate(tariff, balance)
            assert start == estimation.start_date
            assert end == estimation.end_date

    with context("with a different class than REEProfile"):
        with it("must return two months of coefficients"):
            start = TIMEZONE.localize(datetime(2018, 1, 1, 1))
            end = TIMEZONE.localize(datetime(2018, 2, 2, 0))
            tariff = T20A()
            accumulated = 0
            balance = {
                'P1': 6.8,
                'P2': 3,
                'P3': 3.5,
            }

            # Janaury + February
            expected = 768

            profile = Profile(start, end, self.measures, accumulated)
            profile.profile_class = FakeClass

            estimation = profile.estimate(tariff, balance)
            assert expected == estimation.n_hours
            assert not estimation.first_day_of_month
