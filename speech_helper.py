from functools import reduce


def __convert_bin_type(bin_type):
    if 'black bin' == bin_type.lower():
        return 'general rubbish'
    elif 'orange bin' == bin_type.lower():
        return 'recycling'
    elif 'green bin' == bin_type.lower():
        return 'garden'
    else:
        return bin_type


def get_speech_text(schedule, week):
    day_of_week = schedule[1]

    tense_a = schedule[2]
    if 'Future' == tense_a:
        tense_a = 'will be on'
        tense_b = 'will be'
    elif 'Past' == tense_a:
        tense_a = 'was on'
        tense_b = 'was'
    else:
        tense_a = 'is'
        tense_b = 'is'
        day_of_week = 'today'

    collection_types = [__convert_bin_type(bin_type) for bin_type in schedule[0]]
    collections = reduce(lambda a, b: a + ' and ' + b, sorted(collection_types))

    return "{week} weeks collection {tense_a} {day} and {tense_b} {collections}".format(
        week=week,
        tense_a=tense_a,
        tense_b=tense_b,
        day=day_of_week,
        collections=collections)
