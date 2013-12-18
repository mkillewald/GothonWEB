from nose.tools import *
from gothonweb import parser

def test_peek():
    word_list = [('verb', 'open'), ('stop', 'the'), ('noun', 'door')]
    w = parser.WordList(word_list)
    result = w._WordList__peek()
    assert_equal(result, 'verb')

def test_match():
    word_list = [('verb', 'open'), ('stop', 'the'), ('noun', 'door')]
    w = parser.WordList(word_list)
    result = w._WordList__match('verb')
    assert_equal(result, ('verb', 'open'))
    assert_equal(word_list, [('stop', 'the'), ('noun', 'door')]) 
    
def test_skip():
    word_list = [('stop', 'the'), ('noun', 'door')]
    w = parser.WordList(word_list)
    result = w._WordList__skip('stop')
    assert_equal(word_list, [('noun', 'door')])
    
def test_parse_verb():
    word_list = [('stop', 'of'), ('verb', 'open'), ('stop', 'the'), ('noun', 'door')]
    w = parser.WordList(word_list)
    result = w._WordList__parse_verb()
    assert_equal(result, ('verb', 'open'))
    assert_equal(word_list, [('stop', 'the'), ('noun', 'door')])
 
    #word_list = [('noun', 'door')]
    #assert_raises(parser.ParserError, parser.parse_verb, word_list)
    
def test_parse_object():
    word_list = [('stop', 'the'), ('noun', 'door')]
    w = parser.WordList(word_list)
    result = w._WordList__parse_object()
    assert_equal(result, ('noun', 'door'))
    assert_equal(word_list, [])
    
    word_list = [('stop','of'), ('direction', 'east')]
    w = parser.WordList(word_list)
    result = w._WordList__parse_object()
    assert_equal(result, ('direction', 'east'))
    assert_equal(word_list, [])
    
    word_list = [('stop', 'a'), ('number', '1234')]
    w = parser.WordList(word_list)
    result = w._WordList__parse_object()
    assert_equal(result, ('number', '1234'))
    assert_equal(word_list, [])

    #word_list = [('verb', 'open')]
    #assert_raises(parser.ParserError, parser.parse_object, word_list)

def test_parse_subject():
    word_list = [('verb', 'open'), ('stop', 'the'), ('noun', 'door')]
    w = parser.WordList(word_list)
    result = w._WordList__parse_subject(('noun', 'user'))
    assert_equal(result.subject, 'user')
    assert_equal(result.verb, 'open')
    assert_equal(result.object, 'door')

def test_parse_number():
    word_list = [('number', '666')]
    w = parser.WordList(word_list)
    result = w._WordList__parse_number(('noun', 'user'), ('verb', 'typed'))
    assert_equal(result.subject, 'user')
    assert_equal(result.verb, 'typed')
    assert_equal(result.object, '666')

def test_parse_sentence():
    word_list = [('verb', 'open'), ('stop', 'the'), ('noun', 'door')]
    w = parser.WordList(word_list)
    result = w.parse_sentence()
    assert_equal(result.subject, 'player')
    assert_equal(result.verb, 'open')
    assert_equal(result.object, 'door')
    assert_equal(word_list, [])

    word_list = [('noun', 'princess'), ('verb', 'open'), ('stop', 'the'), ('noun', 'door')]
    w = parser.WordList(word_list)
    result = w.parse_sentence()
    assert_equal(result.subject, 'princess')
    assert_equal(result.verb, 'open')
    assert_equal(result.object, 'door')
    assert_equal(word_list, [])

    #word_list = [('error', 'through'), ('stop', 'the'), ('direction', 'north'), ('noun', 'door')]
    #assert_raises(parser.ParserError, parser.parse_sentence, word_list)
