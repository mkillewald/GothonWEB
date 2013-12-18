def convert_numbers(s):
    """
    If input string is a number, returns int
    """

    try:
        return int(s)
    except ValueError:
        return None

def scan(sentence):
    """
    Takes input string and returns a list of tuples. "shoot the bear" becomes
    [('verb', 'shoot'), ('stop', 'the'), ('noun', 'bear')]
    """

    directions = (
        'north', 'south', 'east','west', 'up', 'down', 'left', 'right', 'back', 'forward'
    )
    verbs = (
        'shoot', 'dodge', 'throw', 'place', 'tell', 'help'
    )
    stops = (
        'the', 'in', 'of', 'from', 'at', 'it', 'a', 'with'
    )
    nouns = (
        'joke', 'bomb'
    )
    
    words = sentence.split()
    result = []
    for item in words:
        if item in directions:
            result.append(('direction', item))
        elif item in verbs:
            result.append(('verb', item))
        elif item in stops:
            result.append(('stop', item))
        elif item in nouns:
            result.append(('noun', item))
        elif convert_numbers(item):
            result.append(('number', item))
        else:
            pass
            # word is not defined in lexicon and is skipped
            # wish list: store list of words not understood for manual review and possible addition to lexicon
            #result.append(('error', item))    
    return result

