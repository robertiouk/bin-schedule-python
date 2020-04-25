import requests
from datetime import datetime
from functools import reduce

ADDRESS_BY_POSTCODE_URL = 'https://bbcpro-jeapi.azurewebsites.net/api/addresssearch/bypostcode?Postcode=ab12' \
                          '%23cd&Language=ENG '
COLLECTION_BY_UPRN = 'https://bbaz-as-prod-bartecapi.azurewebsites.net/api/bincollections/residential/getbyuprn' \
                     '/10002965475 '


def __get_week_day_from_entry(entry):
    entry_date = entry['JobScheduledStart']
    date = __get_date_from_string(entry_date)

    return date.isocalendar()[1]


def __get_date_from_string(date_string):
    return datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S')


def __get_weekday_from_date_string(date_string):
    date = __get_date_from_string(date_string)
    return date.strftime('%A')


def __get_temporal_status(date_now, collection_date):
    """Return whether the collection date is in the past, present or future"""
    now_day = date_now.day
    collection_day = collection_date.day
    return 'Past' if now_day > collection_day else 'Future' if now_day < collection_day else 'Present'


def get_collection(week):
    """Use the council API to get the collection for a given date"""

    response = requests.get(COLLECTION_BY_UPRN)

    json = response.json()['BinCollections']
    today = datetime.today()
    current_week = today.isocalendar()[1]
    given_week = current_week if week == 'this' else current_week + 1

    # Will return a list of lists, e.g.,
    # [[], [], [('Green bin', '2020-04-28T00:00:00'), ('Orange bin', '2020-04-28T00:00:00')], []]
    result = [
        [(entry['BinType'], entry['JobScheduledStart'])
         for entry in week_entry
         if __get_week_day_from_entry(entry) == given_week]
        for week_entry in json]
    # Filter out the empty lists
    filtered = list(filter(lambda collections: collections, result))
    # Flatten to: [('Green bin', '2020-04-28T00:00:00'), ('Orange bin', '2020-04-28T00:00:00')]
    flattened = list(reduce(list.__add__, filtered))
    # Map bin type to a list so it can be reduced in the next step, with the collection day and its
    # temporal relation to the present day, e.g.,
    # [(['Green bin'], 'Tuesday', 'Past'), (['Orange bin'], 'Tuesday', 'Past')]
    mapped = list(map(lambda e: ([e[0]],
                                 __get_weekday_from_date_string(e[1]),
                                 __get_temporal_status(today, __get_date_from_string(e[1]))),
                      flattened))
    # Reduce to a list of bins, with the first date that (we don't need the rest as they are duplicates)
    # mapped to a day string, e.g.,
    # (['Green bin', 'Orange bin'], 'Tuesday', 'Past')
    reduced = reduce(lambda a, b: (reduce(list.__add__, [a[0], b[0]]), a[1], a[2]), mapped)

    return reduced
