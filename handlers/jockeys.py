#!/usr/bin/env python

import web

class JockeyContext:

    def __init__(self):
        self.is_new = True
        self.jockey = None

class JockeysHandler:

    def GET(self):
        return web.ctx.render.jockeys(web.ctx.jockeys.get_jockeys())

class JockeysNewHandler:

    def GET(self):
        jockey_context = JockeyContext()
        jockey_context.jockey = web.ctx.jockeys.create_jockey()
        return web.ctx.render.jockey(jockey_context)

class JockeysEditHandler:

    def GET(self, id):
        jockey_context = JockeyContext()
        jockey_context.is_new = False
        jockey_context.jockey = web.ctx.jockeys.get_jockey(id)
        return web.ctx.render.jockey(jockey_context)

class JockeysUpdateHandler:

    def POST(self):
        user_data = web.input(address='', age=0, weight=0, height=0, fullname='', id=None)
        jockey = web.ctx.jockeys.create_jockey()
        jockey.id = user_data.id
        jockey.address = user_data.address
        jockey.age = user_data.age
        jockey.weight = user_data.weight
        jockey.height = user_data.height
        jockey.fullname = user_data.fullname
        if jockey.id is None:
            web.ctx.jockeys.insert_jockey(jockey)
        else:
            web.ctx.jockeys.update_jockey(jockey)
        raise web.seeother('/jockeys')

class JockeysDeleteHandler:

    def GET(self, id):
        if id == 'all':
            web.ctx.jockeys.clear()
        else:
            web.ctx.jockeys.delete_jockey(id)
        raise web.seeother('/jockeys')
