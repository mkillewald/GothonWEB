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
                session.room.show_help = True
                session.room.show_try_again = False
                session.room.go(session.room)
            elif session.room.paths.get(form.action) == None:
                # When form input is not a defined path, use the catch all path '*' if one exists
                if session.room.paths.get('*') == None:
                    session.room.show_try_again = True
                    session.room.show_help = False
                    session.room.go(session.room)
                else:
                    session.room.show_try_again = False
                    session.room.show_help = False
                    session.room = session.room.go('*')
            else:
                session.room.show_try_again = False
                session.room.show_help = False
                session.room = session.room.go(form.action)

        web.seeother("/game")

if __name__ == "__main__":
    app.run()
