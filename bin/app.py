import os
import web
import hashlib
import re

from gothonweb import gothon_map, lexicon, parser


class Index(object):
    def GET(self):
        if logged():
            # this is used to "setup" the session with starting values
            session.room = gothon_map.START()
            web.seeother("/game")
        else:
            web.seeother("/login")

class Login(object):
    def GET(self):
        if logged():
            web.seeother("/")
        else:
            render = create_render(session.privilege)
            return render.login()

    def POST(self):
        name, passwd = web.input().name, web.input().passwd

        try:
            ident = db.select('game_users', where='username=$name', vars=locals())[0]
            if hashlib.sha1("sAlT754-"+passwd).hexdigest() == ident['pass']:
                session.login = 1
                session.privilege = ident['privilege']
                web.seeother("/")
            else:
                session.login = 0 
                session.privilege = 0
                render = create_render(session.privilege)
                return render.login_error()
        except:
            session.login = 0
            session.privilege = 0
            render = create_render(session.privilege)
            return render.login_error()


class Logout(object):
    def GET(self):
        if logged():
            session.login = 0
            session.kill()
            render = create_render(session.privilege)
            return render.logout()
        else:
            web.seeother("/")

class Reset(object):
    def GET(self):
        session.login = 0
        session.kill()
        web.seeother('/')
 
class SignUp(object):
    pass

class ForgetPass(object):
    pass

class GameEngine(object):
    def GET(self):
        if logged():
            if session.room:
                render = create_render(session.privilege)
                return render.show_room(room=session.room)
            else:
                # Something wonderful has happened... 
                render = create_render(session.privilege)
                return render.error()
        else:
            web.seeother("/login")

    def POST(self):
        if logged():
            form = web.input(action=None)

            if session.room and form.action:
                input_list = lexicon.scan(form.action.lower())
                p = parser.Parser(input_list)
                s = p.parse_sentence()
                form_input = s.form_sentence()

                if form_input == "player help":
                    session.room.show_help = True
                    session.room.show_try_again = False
                elif form_input == "player try again":
                    session.room.show_help = False
                    session.room.show_try_again = True
                elif session.room.paths.get(form_input):
                    session.room = session.room.go(form_input)
                elif session.room.filter.match(form_input) and session.room.count > 1:
                    session.room.count -=1
                    session.room.show_help = False
                    session.room.show_try_again = False
                elif session.room.filter.match(form_input) and session.room.paths.get('*'):
                    session.room = session.room.go('*')
                else:
                    session.room.show_try_again = True
                    session.room.show_help = False

            web.seeother("/game")
        else:
            web.seeother("/login")

def logged():
    if session.login == 1:
        return True
    else:
        return False

def create_render(privilege):
    if logged():
        if privilege == 0:
            render = web.template.render('templates/reader', base="../layout")
        elif privilege == 1:
            render = web.template.render('templates/user', base="../layout")
        elif privilege == 2:
            render = web.template.render('templates/admin', base="../layout")
        else:
            render = web.template.render('templates/communs', base="../layout")
    else:
        render = web.template.render('templates/communs', base="../layout")
    return render


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
  '/login', 'Login',
  '/logout', 'Logout',
  '/game', 'GameEngine',
  '/reset', 'Reset',
  '/', 'Index',
)

#app = web.application(urls, globals())
app = web.application(urls, locals())
db = web.database(dbn='postgres', db='GothonWEB', user='vagrant', pw='')

#render = web.template.render('templates/', base="layout")

# little hack so that debug mode works with sessions
if web.config.get('_session') is None:
    store = web.session.DBStore(db, 'sessions')
    #store = web.session.DiskStore('sessions')
    session = web.session.Session(app, store, 
        initializer={'room': None, 'login': 0, 'privilege': 0})
    web.config._session = session
else:
    session = web.config._session

if (not is_test()) and __name__ == "__main__":
    app.run() 