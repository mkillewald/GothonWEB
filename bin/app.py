import os
import web
from gothonweb import gothon_map, lexicon, parser


class Index(object):
    def GET(self):
        # this is used to "setup" the session with starting values
        session.room = gothon_map.START()
        web.seeother("/game")

class Reset(object):
    def GET(self):
        session.kill()
        web.seeother("/")

class GameEngine(object):

    def GET(self):
        if session.room:
            return render.show_room(room=session.room)
        else:
            return render.error()

    def POST(self):
        form = web.input(action=None)

        input_list = lexicon.scan(form.action.lower())
        w = parser.WordList(input_list)
        s = w.parse_sentence()
        form_input = s.form_sentence()

        # there is a bug here, can you fix it? -Zed Shaw
        # If you mean the catch all path was never called, then yes I fixed it. -Mike Killewald
        if session.room and form_input:
            if form_input == "player help":
                # If 'help' was input by user, redisplay room with room.help text.
                session.room.show_help = True
                session.room.show_try_again = False
            elif form_input == "player try again":
                # If user input was not understood, redisplay room with room.try_again text.
                session.room.show_help = False
                session.room.show_try_again = True
            elif session.room.count:
                # If room has a count defined, step through counter until it reaches 0.
                if session.room.paths.get(form_input) == None:
                    session.room.count -= 1
                    if session.room.count > 0:
                        session.room.show_help = False
                        session.room.show_try_again = False
                    else:
                        session.room = session.room.go('*')
                else:
                    session.room = session.room.go(form_input)
            elif session.room.paths.get(form_input) == None:
                # When form input is not a defined path, use the catch all path '*' if one exists
                # If no catch all path exists, redisplay room with try_again text.
                if session.room.paths.get('*') == None:
                    session.room.show_try_again = True
                    session.room.show_help = False
                else:
                    session.room = session.room.go('*')
            else:
                session.room = session.room.go(form_input)

        web.seeother("/game")


def is_test():
    # In order to avoid kicking off web.py's webserver when we run our tests, 
    # we can define an environment variable, such as WEBPY_ENV=test. Then when 
    # we run our tests, it's simply a matter of running nosetests like so:
    #
    # WEBPY_ENV=test nosetests

    if 'WEBPY_ENV' in os.environ:
        return os.environ['WEBPY_ENV'] == 'test'

web.config.debug = False

urls = (
  '/game', 'GameEngine',
  '/reset', 'Reset',
  '/', 'Index',
)

app = web.application(urls, globals())

# little hack so that debug mode works with sessions
if web.config.get('_session') is None:
    store = web.session.DiskStore('sessions')
    session = web.session.Session(app, store,
                                  initializer={'room': None})
    web.config._session = session
else:
    session = web.config._session

render = web.template.render('templates/', base="layout")

if (not is_test()) and __name__ == "__main__":
    app.run()