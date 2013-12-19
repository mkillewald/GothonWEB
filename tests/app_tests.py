from web import net
from nose.tools import *
from paste.fixture import TestApp

from bin.app import app
from gothonweb.gothon_map import *

def start_game():
    middleware = []
    return TestApp(app.wsgifunc(*middleware))

def start_central_corridor():
    testApp = start_game()
    resp = testApp.get('/')
    resp = resp.follow()
    form = resp.forms[0]
    return (testApp, form, resp)

def enter_laser_weapon_armory():
    testApp, form, resp = start_central_corridor()
    form['action'] = 'tell a joke'
    form.submit()
    resp = testApp.get('/game')
    form = resp.forms[0]
    return (testApp, form, resp)

def enter_the_bridge():
    testApp, form, resp = enter_laser_weapon_armory()
    form['action'] = laser_weapon_armory.secret
    form.submit()
    resp = testApp.get('/game')
    form = resp.forms[0]
    return (testApp, form, resp)

def enter_escape_pod():
    testApp, form, resp = enter_the_bridge()
    form['action'] = 'slowly place the bomb'
    form.submit()
    resp = testApp.get('/game')
    form = resp.forms[0]
    return (testApp, form, resp)

def test_index():
    testApp = start_game()
    
    # check that we get a 303 on the / URL 
    # because it redirects to /game through GameEngine
    resp = testApp.get('/')
    assert_equal(resp.status, 303)
    
    # check that /game loads correct room on start
    resp = testApp.get('/game')
    assert_equal(resp.status, 200)
    resp.mustcontain(net.htmlquote(central_corridor.description))
    testApp.get('/reset')
    testApp.reset()

def test_central_corridor():
    testApp, form, resp = start_central_corridor()

    # test try again
    form['action'] = 'iadsjklds'
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain(net.htmlquote(central_corridor.try_again))

    # test help
    form['action'] = 'help'
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain(net.htmlquote(central_corridor.help))

    # test path to Laser Weapon Armory
    form['action'] = 'tell a joke'
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain(net.htmlquote(laser_weapon_armory.description))
    testApp.get('/reset')
    testApp.reset()

def test_central_corridor_shoot():
    testApp, form, resp = start_central_corridor()

    # test shoot death
    form['action'] = 'shoot'
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain(net.htmlquote(central_corridor_shoot.description))
    testApp.get('/reset')
    testApp.reset()

def test_central_corridor_dodge():
    testApp, form, resp = start_central_corridor()

    # test dodge death
    form['action'] = 'dodge'
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain(net.htmlquote(central_corridor_dodge.description))
    testApp.get('/reset')
    testApp.reset()

def test_laser_weapon_armory_guesses():
    testApp, form, resp = enter_laser_weapon_armory()

    # test help
    form['action'] = 'help'
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain(net.htmlquote(laser_weapon_armory.help))

    # test invalid input
    form['action'] = '1'
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain('You have 10 tries left')
    resp.mustcontain(net.htmlquote(laser_weapon_armory.try_again))
    form['action'] = 'tell a joke'
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain('You have 10 tries left')
    resp.mustcontain(net.htmlquote(laser_weapon_armory.try_again))
    form['action'] = 'fuck you'
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain('You have 10 tries left')
    resp.mustcontain(net.htmlquote(laser_weapon_armory.try_again))

    # test 10 wrong guesses
    if laser_weapon_armory.secret == '999':
        test_input = '998'
    else:
        test_input = '999'
    resp.mustcontain('You have 10 tries left')
    form['action'] = test_input
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain('You have 9 tries left')
    form['action'] = test_input
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain('You have 8 tries left')
    form['action'] = test_input
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain('You have 7 tries left')
    form['action'] = test_input
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain('You have 6 tries left')
    form['action'] = test_input
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain('You have 5 tries left')
    form['action'] = test_input
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain('You have 4 tries left')

    # Test help in between lock code attempts. This should not 
    # alter number of guesses used or remaining. 
    form['action'] = 'help'
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain(net.htmlquote(laser_weapon_armory.help))

    # continue checking remaining guesses
    form['action'] = test_input
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain('You have 3 tries left')
    form['action'] = test_input
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain('You have 2 tries left')
    form['action'] = test_input
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain('You have 1 try left')

    #last guess, a wrong entry here should equal death
    form['action'] = test_input
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain(net.htmlquote(laser_weapon_armory_death.description))
    testApp.get('/reset')
    testApp.reset()

def test_laser_weapon_armory_lock():
    # test lock code on first guess
    testApp, form, resp = enter_laser_weapon_armory()
    form['action'] = laser_weapon_armory.secret
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain(net.htmlquote(the_bridge.description))
    testApp.get('/reset')
    testApp.reset()

    # test lock code after displaying help
    testApp, form, resp = enter_laser_weapon_armory()
    form['action'] = 'help'
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain(net.htmlquote(laser_weapon_armory.help))
    form['action'] = laser_weapon_armory.secret
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain(net.htmlquote(the_bridge.description))
    testApp.get('/reset')
    testApp.reset()

    # test lock code after wrong guesses
    if laser_weapon_armory.secret == '999':
        test_input = '998'
    else:
        test_input = '999'
    testApp, form, resp = enter_laser_weapon_armory()
    form['action'] = test_input
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain('You have 9 tries left')
    form['action'] = test_input
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain('You have 8 tries left')
    form['action'] = laser_weapon_armory.secret
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain(net.htmlquote(the_bridge.description))
    testApp.get('/reset')
    testApp.reset()

    # test lock code after invalid input
    # Case 1: input not recognized by lexicon
    testApp, form, resp = enter_laser_weapon_armory()
    form['action'] = 'fuck you'
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain('You have 10 tries left')
    resp.mustcontain(net.htmlquote(laser_weapon_armory.try_again))
    form['action'] = laser_weapon_armory.secret
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain(net.htmlquote(the_bridge.description))
    testApp.get('/reset')
    testApp.reset()

    # test lock code after invalid input
    # Case 2: input recognized by lexicon, but does not match room.filter
    testApp, form, resp = enter_laser_weapon_armory()
    form['action'] = 'tell a joke'
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain('You have 10 tries left')
    resp.mustcontain(net.htmlquote(laser_weapon_armory.try_again))
    form['action'] = laser_weapon_armory.secret
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain(net.htmlquote(the_bridge.description))
    testApp.get('/reset')
    testApp.reset()

    # test lock code after invalid input
    # Case 3: Not enough digits. (does not match room.filter)
    testApp, form, resp = enter_laser_weapon_armory()
    form['action'] = '1'
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain('You have 10 tries left')
    resp.mustcontain(net.htmlquote(laser_weapon_armory.try_again))
    form['action'] = laser_weapon_armory.secret
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain(net.htmlquote(the_bridge.description))
    testApp.get('/reset')
    testApp.reset()

def test_the_bridge():
    testApp, form, resp = enter_the_bridge()

    # test try again
    form['action'] = 'iadsjklds'
    form.method = 'POST'
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain(net.htmlquote(the_bridge.try_again))

    # test help
    form['action'] = 'help'
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain(net.htmlquote(the_bridge.help))

    # test path to Escape Pod
    form['action'] = 'slowly place the bomb'
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain(net.htmlquote(escape_pod.description))
    testApp.get('/reset')
    testApp.reset()

def test_the_bridge_death():
    testApp, form, resp = enter_the_bridge()

    # test the_bridge death
    form['action'] = 'throw the bomb'
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain(net.htmlquote(the_bridge_death.description))
    testApp.get('/reset')
    testApp.reset()

def test_escape_pod():
    testApp, form, resp = enter_escape_pod()

    # test invalid input
    # Case 1: digit not 1-5
    form['action'] = '9'
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain(net.htmlquote(escape_pod.try_again))

    # test invalid input
    # Case 2: input not in lexicon
    form['action'] = 'fuck you'
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain(net.htmlquote(escape_pod.try_again))

    # test invalid input
    # Case 3: input in lexicon, but does not match room.filter
    form['action'] = 'tell a joke'
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain(net.htmlquote(escape_pod.try_again))

    # test help
    form['action'] = 'help'
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain(net.htmlquote(escape_pod.help))

    # test path to the_end_winner
    form['action'] = escape_pod.secret
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain(net.htmlquote(the_end_winner.description))
    testApp.get('/reset')
    testApp.reset()

def test_escape_pod_death():
    testApp, form, resp = enter_escape_pod()

    #test path to the_end_loser
    if escape_pod.secret == '1':
        test_input = '2'
    else:
        test_input = '1'
    form['action'] = test_input
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain(net.htmlquote(the_end_loser.description))
    testApp.get('/reset')
    testApp.reset()
