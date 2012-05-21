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

class HorsesEditHandler:

    def GET(self, id):
        horse_context = HorseContext()
        horse_context.is_new = False
        horse_context.horse = web.ctx.horses.get_horse(id)
        horse_context.owners = web.ctx.owners.get_owners()
        return web.ctx.render.horse(horse_context)

class HorsesUpdateHandler:

    def POST(self):
        user_data = web.input(nickname='', sex='', age=1, owner_id=None, id=None)
        horse = web.ctx.horses.create_horse()
        horse.id = user_data.id
        horse.nickname = user_data.nickname
        horse.sex = user_data.sex
        horse.age = int(user_data.age)
        horse.owner_id = user_data.owner_id
        if horse.id is None:
            web.ctx.horses.insert_horse(horse)
        else:
            web.ctx.horses.update_horse(horse)
        raise web.seeother('/horses')

class HorsesDeleteHandler:

    def GET(self, id):
        if id != 'all':
            web.ctx.horses.delete_horse(id)
        else:
            web.ctx.horses.clear()
        raise web.seeother('/horses')
