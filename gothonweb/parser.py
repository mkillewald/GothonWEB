# Usage:
# s = lexicon.scan("shoot the fucking bear")
# w = WordList(s)
# s = w.parse_sentence()
# >>> print s.subject, s.verb, s.object
# >>> player shoot bear


class ParserError(Exception):
    pass


class Sentence(object):

    def __init__(self, subject, verb, object):
        self.subject = subject[1]
        self.verb = verb[1]
        self.object = object[1]


class WordList(object):
    """
    Use parse_sentence method to convert list of tuples from lexicon.scan into a Sentence object. 

    """

    def __init__(self, word_list):
        self.word_list = word_list

    def __peek(self):
        if self.word_list:
            word = self.word_list[0]
            return word[0]
        else:
            return None


    def __match(self, expecting):
        if self.word_list:
            word = self.word_list.pop(0)

            if word[0] == expecting:
                return word
            else:
                return None
        else:
            return None


    def __skip(self, word_type):
        while self.__peek() == word_type:
            self.__match(word_type)


    def __parse_verb(self):
        self.__skip('stop')
     
        if self.__peek() == 'verb':
            return self.__match('verb')
        else:
            raise ParserError("Expected a verb next. Instead saw %s next." % next)


    def __parse_object(self):
        self.__skip('stop')
        next = self.__peek()

        if next == 'noun':
            return self.__match('noun')
        if next == 'direction':
            return self.__match('direction')
        if next == 'number':
            return self.__match('number')
        else:
            raise ParserError("Expected a noun, direction or number next. Instead saw %s next." % next)


    def __parse_subject(self, subj): 
        verb = self.__parse_verb()
        self.__skip('stop')

        if self.word_list:
            obj = self.__parse_object()
        else:
            # word_list is empty, no object for verb to act on. 
            obj = ('noun', '')

        return Sentence(subj, verb, obj)

    def __parse_number(self, subj, verb):
        obj = self.__parse_object()

        return Sentence(subj, verb, obj)

    def parse_sentence(self):
        self.__skip('stop')
     
        start = self.__peek()

        if start == 'noun':
            subj = self.__match('noun')
            return self.__parse_subject(subj)
        elif start == 'verb':
            # assume the subject is the player then
            return self.__parse_subject(('noun', 'player'))
        elif start == 'number':
            # assume the subjext is the player and the verb is 'entered'
            return self.__parse_number(('noun', 'player'), ('verb', 'entered'))
        elif start == None:
            # word_list is empty and probably contained words not in lexicon
            return Sentence(('noun', 'player'), ('verb', 'try again'), ('noun', ''))
        else:
            raise ParserError("Must start with subject, object, or verb not: %s" % start)
