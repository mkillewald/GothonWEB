import os
import web
import re
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
            # Something wonderful has happened... 
            return render.error()

    def POST(self):
        form = web.input(action=None)

        input_list = lexicon.scan(form.action.lower())
        w = parser.WordList(input_list)
        s = w.parse_sentence()
        form_input = s.form_sentence()

        if session.room and form_input:
            if form_input == "player help":
                # 'help' was input by user, redisplay room with room.help text.
                session.room.show_help = True
                session.room.show_try_again = False
            elif form_input == "player try again":
                # Form input was not understood by lexicon, redisplay room with room.try_again text.
                session.room.show_help = False
                session.room.show_try_again = True
            elif session.room.paths.get(form_input) == None:
                # Form input is understood by lexicon, but is not in room.paths. 
                if session.room.filter.match(form_input) and session.room.count > 1:
                    # Form input matches room.filter and count is greater than 1, so
                    # decrement counter and redisplay room
                    session.room.count -=1
                    session.room.show_help = False
                    session.room.show_try_again = False
                elif session.room.filter.match(form_input) and session.room.paths.get('*'):
                    # room.count either doesn't exist of is less than 1, a catch all path '*' exists and
                    # form input matches room.filter, so lets follow the '*' path
                    session.room = session.room.go('*')
                else:
                    # Form input does not match room.filter, or no catch all path exists,
                    # redisplay room with room.try_again text.
                    session.room.show_try_again = True
                    session.room.show_help = False
            else:
                # Form input is understood and is a defined path. 
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