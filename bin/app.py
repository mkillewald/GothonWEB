import os
import web
import hashlib
import re

from gothonweb import gothon_map, lexicon, parser

class Login(object):
    def GET(self):
        if logged():
            web.seeother("/")
        else:
            render = create_render(session.privilege)
            return render.login(message=None)

    def POST(self):
        name, passwd = web.input().name, web.input().passwd

        try:
            ident = db.select('game_users', where='username=$name', vars=locals())[0]
            if hashlib.sha1("sAlT754-"+passwd).hexdigest() == ident['passwd']:
                session.login = 1
                session.privilege = ident['privilege']
                session.username = ident['username']
                # this is used to "setup" the session with starting values
                session.room = gothon_map.START()
                web.seeother("/game")
            else:
                session.login = 0 
                session.privilege = 0
                render = create_render(session.privilege)
                return render.login(message="Password incorrect, please try again.")
        except:
            session.login = 0
            session.privilege = 0
            render = create_render(session.privilege)
            return render.login(message="Username invalid, please try again.")

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
        if logged():
            session.login = 0
            session.kill()
            render = create_render(session.privilege)
            return render.logout()
        else:
            web.seeother("/")
 
class Register(object):
    def GET(self):
        if logged():
            web.seeother("/")
        else:
            render = create_render(session.privilege)
            return render.register(message="All fields are required.")

    def POST(self):
        if logged():
            web.seeother("/")
        else:
            name, passwd, email = web.input().name, web.input().passwd, web.input().email
            if name == '' or passwd == '' or email == '':
                render = create_render(session.privilege)
                return render.register(message="All fields are required, please try again.")
            else:
                try:
                    match_username = db.select('game_users', where='username=$name', vars=locals())[0]
                    render = create_render(session.privilege)
                    return render.register(message="Username already exists, please try again.")
                except:
                    match_username = False

                try:
                    match_email = db.select('game_users', where='email=$email', vars=locals())[0]
                    render = create_render(session.privilege)
                    return render.register(message="E-mail address already exists, please try again.")
                except:
                    match_email = False

                if not match_email and not match_username:
                    try:
                        passwd = hashlib.sha1("sAlT754-"+passwd).hexdigest()
                        add_user = db.insert('game_users', username=name, passwd=passwd, email=email, privilege=0)
                        render = create_render(session.privilege)
                        return render.login(message="Registration successful, please login:")
                    except:
                        render = create_render(session.privilege)
                        return render.register(message="Registration failed, please try again.")

class ForgotPass(object):
    pass

class Index(object):
    def GET(self):
        if logged():
            web.seeother("/game")
        else:
            web.seeother("/login")

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
    try:
        if session.login == 1:
            return True
        else:
            return False
    except:
        return False

def create_render(privilege):
    if logged():
        if privilege == 0:
            render = web.template.render('templates/reader', base="../layout", globals={'context': session})
        elif privilege == 1:
            render = web.template.render('templates/user', base="../layout", globals={'context': session})
        elif privilege == 2:
            render = web.template.render('templates/admin', base="../layout", globals={'context': session})
        else:
            render = web.template.render('templates/communs', base="../layout", globals={'context': session})
    else:
        render = web.template.render('templates/communs', base="../layout", globals={'context': session})
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
  '/register', 'Register',
  '/game', 'GameEngine',
  '/reset', 'Reset',
  '/', 'Index',
)

app = web.application(urls, globals())
db = web.database(dbn='postgres', db='GothonWEB', user='vagrant', pw='')

# little hack so that debug mode works with sessions
if web.config.get('_session') is None:
    store = web.session.DBStore(db, 'sessions')
    session = web.session.Session(app, store, 
        initializer={'room': None, 'login': 0, 'privilege': 0, 'username': None})
    web.config._session = session
else:
    session = web.config._session

if (not is_test()) and __name__ == "__main__":
    app.run() 