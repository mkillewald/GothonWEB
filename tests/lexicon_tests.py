from nose.tools import *
from gothonweb import lexicon

def test_directions():
    assert_equal(lexicon.scan("north"), [('direction', 'north')])
    result = lexicon.scan("north south east")
    assert_equal(result, [('direction', 'north'),
                          ('direction', 'south'),
                          ('direction', 'east')])

def test_verbs():
    assert_equal(lexicon.scan("shoot"), [('verb', 'shoot')])
    result = lexicon.scan("shoot dodge throw")
    assert_equal(result, [('verb', 'shoot'),
                          ('verb', 'dodge'),
                          ('verb', 'throw')])


def test_stops():
    assert_equal(lexicon.scan("the"), [('stop', 'the')])
    result = lexicon.scan("the in of")
    assert_equal(result, [('stop', 'the'),
                          ('stop', 'in'),
                          ('stop', 'of')])


def test_nouns():
    assert_equal(lexicon.scan("joke"), [('noun', 'joke')])
    result = lexicon.scan("joke bomb")
    assert_equal(result, [('noun', 'joke'),
                          ('noun', 'bomb')])

def test_numbers():
    assert_equal(lexicon.scan("1234"), [('number', '1234')])
    result = lexicon.scan("3 91234")
    assert_equal(result, [('number', '3'),
                          ('number', '91234')])


def test_errors():
    assert_equal(lexicon.scan("ASDFADFASDF"), [])
    result = lexicon.scan("tell a IAS joke")
    assert_equal(result, [('verb', 'tell'),
                          ('stop', 'a'),
                          ('noun', 'joke')])