from unittest import TestCase
import bin_schedule_api


class TestBinScheduleApi(TestCase):
    def test_get_collection(self):
        print(bin_schedule_api.get_collection('this'))
