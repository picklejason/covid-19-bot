import datetime


FORMAT_KEYS = {
    'todayCases': 'Cases Today',
    'todayDeaths': 'Deaths Today',
    'casesPerOneMillion': 'Cases per 1M',
    'deathsPerOneMillion': 'Deaths per 1M',
    'testsPerOneMillion': 'Tests per 1M',
}
TIMESTAMP_KEY = 'updated'
TIMESTAMP_FORMAT = '%Y/%m/%d - %H:%M:%S UTC'


def stats_formatter(response):
    """ applies formatting rules to a stats response object
    """
    response['content'] = [
        {
            'name': keys_formatter(i['name']),
            'value': value_formatter(i['name'], i['value']),
        }
        for i in response['content']
    ]
    return response


def value_formatter(key, value):
    """ formates values with commas inserted, i.e. 10000 -> 10,000
    """
    if key == TIMESTAMP_KEY:
        value /= 1000
        dt = datetime.datetime.fromtimestamp(value, tz=datetime.timezone.utc)
        return dt.strftime(TIMESTAMP_FORMAT)

    return f'{int(value):,}'


def keys_formatter(key):
    """ returns custom readable formatm, else title version of key
    """
    if key in FORMAT_KEYS:
        new_key = FORMAT_KEYS[key]
    else:
        new_key = key.title()
    return new_key + ':'


if __name__ == '__main__':
    import json
    import pprint
    import sys

    with open(sys.argv[1], 'r') as fp:
        countries = json.load(fp)

    info = countries[100]
    response = {
        'description': '',
        'content': []
    }
    for k, v in info.items():
        if k == 'country':  # don't add country lol
            continue
        response['content'].append(
            {
                'name': k,
                'value': v
            }
        )
    response = stats_formatter(response)
    pprint.pprint(response)
