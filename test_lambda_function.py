from unittest import TestCase
import lambda_function


class Test(TestCase):
    def test_lambda_handler_current_schedule_intent(self):
        event = {
            'request': {
                'type': 'IntentRequest',
                'requestId': 'spam',
                'intent': {
                    'name': 'CurrentScheduleIntent'
                }
            },
            'session': {
                'sessionId': 'eggs'
            }
        }

        result = lambda_function.lambda_handler(event, '')

        text = result['response']['outputSpeech']['text']
        print(text)

    def test_lambda_handler_next_schedule_intent(self):
        event = {
            'request': {
                'type': 'IntentRequest',
                'requestId': 'spam',
                'intent': {
                    'name': 'NextScheduleIntent'
                }
            },
            'session': {
                'sessionId': 'eggs'
            }
        }

        result = lambda_function.lambda_handler(event, '')

        text = result['response']['outputSpeech']['text']
        print(text)
