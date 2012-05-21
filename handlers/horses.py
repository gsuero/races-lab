#!/usr/bin/env python

import web

class HorseContext:

    def __init__(self):
        self.is_new = True
        self.horse = None
        self.owners = tuple()

class HorsesHandler:

    def GET(self):
        return web.ctx.render.horses(web.ctx.horses.get_horses())

class HorsesNewHandler:

    def GET(self):
        horse_context = HorseContext()
        horse_context.horse = web.ctx.horses.create_horse()
        horse_context.owners = web.ctx.owners.get_owners()
        return web.ctx.render.horse(horse_context)
