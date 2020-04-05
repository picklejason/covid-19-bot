FORMAT_KEYS = {
    'todayCases': 'Cases Today',
    'todayDeaths': 'Deaths Today',
    'casesPerOneMillion': 'Cases per 1M',
    'deathsPerOneMillion': 'Deaths per 1M'
}


def stats_formatter(response):
    """ applies formatting rules to a stats response object
    """
    response['content'] = [
        {
            'name': keys_formatter(i['name']),
            'value': value_formatter(i['value']),
        }
        for i in response['content']
    ]
    return response


def value_formatter(value):
    """ formates values with commas inserted, i.e. 10000 -> 10,000
    """
    return f'{int(value):,}'


def keys_formatter(key):
    """ returns custom readable formatm, else title version of key
    """
    if key in FORMAT_KEYS:
        new_key = FORMAT_KEYS[key]
    else:
        new_key = key.title()
    return new_key + ':'
