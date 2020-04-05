
__HELP_DATA = {}
__ALIASES = {}
__REVERSE_ALIASES = {}


def add_help(command, aliases, text):
    """ Add help text for a command.
    """
    __HELP_DATA[command] = text
    __REVERSE_ALIASES[command] = aliases
    __ALIASES.update({a: command for a in aliases})


def clear_help():
    """ Flush the help data
    """
    __HELP_DATA.clear()
    __ALIASES.clear()
    __REVERSE_ALIASES.clear()


def get_help(command):
    """ Lookup the help text for a command
    """
    NOT_FOUND = 'That command does not exist'

    text = __HELP_DATA.get(command, '')
    if text:
        return text

    command = __ALIASES.get(command, '')
    return __HELP_DATA.get(command, NOT_FOUND)


def list_aliases(command):
    """ Return a list of aliases for a command
    """
    return __REVERSE_ALIASES.get(command, [])


def list_commands():
    """ Return a list of the commands we can provide help for.
    """
    return sorted(__HELP_DATA)
