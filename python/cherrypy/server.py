#! /usr/bin/env python3
import cherrypy


IS_STANDALONE = __name__ == "__main__"


class WebRoot:
    @cherrypy.expose
    @staticmethod
    def index():
        return ""


@cherrypy.expose
class UserAPI:
    @staticmethod
    def GET(user_id):
        return user_id

    @staticmethod
    def POST():
        return ""


WebRoot.user = UserAPI()


global_config = {"environment": "production" if IS_STANDALONE else "embedded"}
config = {"/user": {"request.dispatch": cherrypy.dispatch.MethodDispatcher()}}


cherrypy.config.update(global_config)

if not IS_STANDALONE:
    # on top of another WSGI server
    # https://docs.cherrypy.org/en/latest/deploy.html#uwsgi
    cherrypy.server.unsubscribe()
    cherrypy.engine.start()

app = cherrypy.tree.mount(WebRoot(), "", config)


# standalone self-test
# python3 -m this_module_name
IS_STANDALONE and cherrypy.quickstart(app)
