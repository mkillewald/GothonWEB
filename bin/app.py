import web
from gothonweb import map

urls = (
  '/game', 'GameEngine',
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


class Index(object):
    def GET(self):
        # this is used to "setup" the session with starting values
        session.room = map.START()
        web.seeother("/game")


class GameEngine(object):

    def GET(self):
        if session.room:
            return render.show_room(room=session.room)
        else:
            return render.error()

    def POST(self):
        form = web.input(action=None)

        # there is a bug here, can you fix it? -Zed Shaw
        # If you mean the catch all path was never called, then yes I fixed it. -Mike Killewald
        if session.room and form.action:
            if form.action == "help":
                # If 'help' was input by user, redisplay room with help text.
                session.room.show_help = True
                session.room.show_try_again = False
            elif session.room.count:
                # If room has a count defined, step through counter
                if session.room.paths.get(form.action) == None:
                    session.room.count -= 1
                    if session.room.count > 0:
                        session.room.show_help = False
                        session.room.show_try_again = False
                    else:
                        session.room = session.room.go('*')
                else:
                    session.room = session.room.go(form.action)
            elif session.room.paths.get(form.action) == None:
                # When form input is not a defined path, use the catch all path '*' if one exists
                # If no catch all path exists, redispaly room with try_again text.
                if session.room.paths.get('*') == None:
                    session.room.show_try_again = True
                    session.room.show_help = False
                else:
                    session.room = session.room.go('*')
            else:
                session.room = session.room.go(form.action)

        web.seeother("/game")

if __name__ == "__main__":
    app.run()