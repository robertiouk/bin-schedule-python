import unittest
import speech_helper


class TestSpeechHelper(unittest.TestCase):
    def test_get_speech_text_single_collection_past(self):
        actual = speech_helper.get_speech_text((['Black bin'], 'Tuesday', 'Past'), 'this')
        self.assertEqual('this weeks collection was on Tuesday and was general rubbish', actual)

    def test_get_speech_text_single_collection_future(self):
        actual = speech_helper.get_speech_text((['Orange bin'], 'Tuesday', 'Future'), 'next')

        self.assertEqual('next weeks collection will be on Tuesday and will be recycling', actual)

    def test_get_speech_text_single_collection_today(self):
        actual = speech_helper.get_speech_text((['Green bin'], 'Tuesday', 'Present'), 'this')

        self.assertEqual('this weeks collection is today and is garden', actual)

    def test_get_speech_text_multiple(self):
        actual = speech_helper.get_speech_text((['Orange bin', 'Green bin'], 'Tuesday', 'Future'), 'next')

        self.assertEqual('next weeks collection will be on Tuesday and will be garden and recycling', actual)

    def test_get_speech_text_with_unknown_bin_type(self):
        actual = speech_helper.get_speech_text((['Orange bin', 'Green bin', 'Ham'], 'Tuesday', 'Future'), 'next')

        self.assertEqual('next weeks collection will be on Tuesday and will be Ham and garden and recycling', actual)


if __name__ == '__main__':
    unittest.main()
