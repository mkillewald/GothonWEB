from nose.tools import *
from bin.app import app
from tests.tools import assert_response

def test_index():
    # check that we get a 303 on the / URL 
    # because it redirects to /game through GameEngine
    resp = app.request("/")
    assert_response(resp, status="303")

    # test our first GET request to /game
    resp = app.request("/game")
    assert_response(resp, status="200")

    # make sure default values work for the form
    resp = app.request("/game", method="POST")
    #assert_response(resp, contains="Central Corridor")

    # test that we get expected values
    data = {"acton": "tell a joke"}
    resp = app.request("/game", method="POST", data=data)
    #assert_response(resp, contains="Laser Weapon Armory")
