from unittest import TestCase
import bin_schedule_api
from datetime import datetime


class TestBinScheduleApi(TestCase):
    def test_get_collection(self):
        print(bin_schedule_api.get_collection('next'))

    def test_get_temporal_status_past(self):
        today = datetime.strptime("2020-04-27T07:52:13", '%Y-%m-%dT%H:%M:%S')
        last = datetime.strptime("2020-04-05T00:00:00", '%Y-%m-%dT%H:%M:%S')

        actual = bin_schedule_api.__get_temporal_status(today, last)

        TestCase.assertEqual(self, 'Past', actual)

    def test_get_temporal_status_month_boundary(self):
        today = datetime.strptime("2020-04-27T07:52:13", '%Y-%m-%dT%H:%M:%S')
        next = datetime.strptime("2020-05-05T00:00:00", '%Y-%m-%dT%H:%M:%S')

        actual = bin_schedule_api.__get_temporal_status(today, next)

        TestCase.assertEqual(self, 'Future', actual)

    def test_get_temporal_status_year_boundary(self):
        today = datetime.strptime("2020-12-31T07:52:13", '%Y-%m-%dT%H:%M:%S')
        next = datetime.strptime("2021-01-05T00:01:05", '%Y-%m-%dT%H:%M:%S')

        actual = bin_schedule_api.__get_temporal_status(today, next)

        TestCase.assertEqual(self, 'Future', actual)



