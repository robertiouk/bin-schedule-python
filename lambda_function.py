import json
import bin_schedule_api
import speech_helper


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could

    add those here

    """

    session_attributes = {}

    card_title = "Welcome"

    speech_output = "Welcome to the Bin Day Schedule Helper, you can ask when the next bin collection is, what the " \
                    "current bin cycle is, and more. "

    reprompt_text = speech_output

    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(

        card_title, speech_output, reprompt_text, should_end_session))


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent['name']

    print(intent_name)

    # Dispatch to your skill's intent handlers
    if "CurrentScheduleIntent" == intent_name:
        return __get_bin_schedule(intent_name, 'this')
    elif "NextScheduleIntent" == intent_name:
        return __get_bin_schedule(intent_name, 'next')
    else:
        raise ValueError("Invalid intent")


def lambda_handler(event, context):
    if event['request']['type'] == 'LaunchRequest':
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    else:
        return {
            'statusCode': 200,
            'body': json.dumps('Hello from Lambda!')
        }


def __get_bin_schedule(intent, request_type):
    card_title = intent
    session_attributes = {}
    should_end_session = True
    reprompt_text = ''

    schedule = bin_schedule_api.get_collection(request_type)
    speech_output = speech_helper.get_speech_text(schedule, request_type)

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
