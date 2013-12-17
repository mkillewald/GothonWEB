def convert_numbers(s):
    try:
        return int(s)
    except ValueError:
        return None

def scan(sentence):
    # returns a list of tuples. "shoot the bear" becomes
    # [('verb', 'shoot'), ('stop', 'the'), ('noun', 'bear')]
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
            #result.append(('error', item))    
    return result

