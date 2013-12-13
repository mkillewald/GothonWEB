from nose.tools import *
from paste.fixture import TestApp
from bin.app import app

# This will generate a new session for each test. remember to delete session files after running tests. 

def test_index():
    middleware = []
    testApp = TestApp(app.wsgifunc(*middleware))
    
    # check that we get a 303 on the / URL 
    # because it redirects to /game through GameEngine
    resp = testApp.get('/')
    assert_equal(resp.status, 303)
    
    # check that /game loads correct room on start
    resp = testApp.get('/game')
    assert_equal(resp.status, 200)
    resp.mustcontain('Central Corridor')

def test_central_corridor():
    middleware = []
    testApp = TestApp(app.wsgifunc(*middleware))
    resp = testApp.get('/')
    resp = resp.follow()

    # test try again
    form = resp.forms[0]
    form['action'] = 'iadsjklds'
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain('try again')

    # test help
    form['action'] = 'help'
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain('tell a joke')

    # test path to Laser Weapon Armory
    form = resp.forms[0]
    form['action'] = 'tell a joke'
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain('Laser Weapon Armory')

def test_central_corridor_shoot():
    middleware = []
    testApp = TestApp(app.wsgifunc(*middleware))
    resp = testApp.get('/')
    resp = resp.follow()

    # test shoot death
    form = resp.forms[0]
    form['action'] = 'shoot'
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain('Shoot, you died!')

def test_central_corridor_dodge():
    middleware = []
    testApp = TestApp(app.wsgifunc(*middleware))
    resp = testApp.get('/')
    resp = resp.follow()

    # test shoot death
    form = resp.forms[0]
    form['action'] = 'dodge'
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain('Sorry, you died!')

def test_laser_weapon_armory():
    middleware = []
    testApp = TestApp(app.wsgifunc(*middleware))
    resp = testApp.get('/')
    resp = resp.follow()

    form = resp.forms[0]
    form['action'] = 'tell a joke'
    form.submit()

    # test help
    form['action'] = 'help'
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain('Hint: Pick a number between')

    # test 10 tries
    resp.mustcontain('You have 10 tries left')
    form['action'] = '1'
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain('You have 9 tries left')
    form['action'] = '2'
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain('You have 8 tries left')
    form['action'] = '3'
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain('You have 7 tries left')
    form['action'] = '4'
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain('You have 6 tries left')
    form['action'] = '5'
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain('You have 5 tries left')
    form['action'] = '6'
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain('You have 4 tries left')

    # Test help in between lock code attemps. This should not 
    # alter number of tries used or remaining. 
    form['action'] = 'help'
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain('Hint: Pick a number between')

    # continue checking remaining tries
    form['action'] = '7'
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain('You have 3 tries left')
    form['action'] = '8'
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain('You have 2 tries left')
    form['action'] = '9'
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain('You have 1 try left')
    form['action'] = '10'
    form.submit()
    resp = testApp.get('/game')
    resp.mustcontain('The lock buzzes one last time')

## Need some way of getting lock_code into tests to go further. 