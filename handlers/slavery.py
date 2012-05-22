#!/usr/bin/env python

import web

class SlaveryContext:

    def __init__(self):
        self.is_new = True
        self.horse_jockey = None
        self.horses = tuple()
        self.jockeys = tuple()

class SlaveryHandler:

    def GET(self):
        return web.ctx.render.slaveries(web.ctx.slaveries.get_horse_jockeys())

class SlaveryNewHandler:

    def GET(self):
        slavery_context = SlaveryContext()
        slavery_context.horse_jockey = web.ctx.slaveries.create_horse_jockey()
        slavery_context.horses = web.ctx.horses.get_horses()
        slavery_context.jockeys = web.ctx.jockeys.get_jockeys()
        return web.ctx.render.slavery(slavery_context)

class SlaveryEditHandler:

    def GET(self, horse_id, jockey_id):
        slavery_context = SlaveryContext()
        slavery_context.is_new = False
        slavery_context.horse_jockey = web.ctx.slaveries.get_horse_jockey(horse_id, jockey_id)
        slavery_context.horses = web.ctx.horses.get_horses()
        slavery_context.jockeys = web.ctx.jockeys.get_jockeys()
        return web.ctx.render.slavery(slavery_context)

class SlaveryUpdateHandler:

    def POST(self):
        user_data = web.input(horse_id=None, jockey_id=None)
        horse_jockey = web.ctx.slaveries.create_horse_jockey()
        horse_jockey.horse_id = user_data.horse_id
        horse_jockey.jockey_id = user_data.jockey_id
        horse_jockey.from_date = user_data.from_date
        horse_jockey.due_date = user_data.due_date
        if web.ctx.slaveries.get_horse_jockey(horse_jockey.horse_id, horse_jockey.jockey_id) is None:
            web.ctx.slaveries.insert_horse_jockey(horse_jockey)
        else:
            web.ctx.slaveries.update_horse_jockey(horse_jockey)
        raise web.seeother('/slavery')

class SlaveryDeleteHandler:

    def GET(self, horse_id, jockey_id):
        web.ctx.slaveries.delete_horse_jockey(horse_id, jockey_id)
        raise web.seeother('/slavery')
