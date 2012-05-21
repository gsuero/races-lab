#!/usr/bin/env python

import web

class OwnerContext:

    def __init__(self):
        self.is_new = True
        self.owner = None

class OwnersHandler:

    def GET(self):
        return web.ctx.render.owners(web.ctx.owners.get_owners())

class OwnersNewHandler:

    def GET(self):
        owner_context = OwnerContext()
        owner_context.owner = web.ctx.owners.create_owner()
        return web.ctx.render.owner(owner_context)

class OwnersEditHandler:

    def GET(self, id):
        owner_context = OwnerContext()
        owner_context.is_new = False
        owner_context.owner = web.ctx.owners.get_owner(id)
        return web.ctx.render.owner(owner_context)

class OwnersUpdateHandler:

    def POST(self):
        user_data = web.input(fullname='', address='', id=None)
        owner = web.ctx.owners.create_owner()
        owner.id = user_data.id
        owner.fullname = user_data.fullname
        owner.address = user_data.address
        if owner.id is None:
            web.ctx.owners.insert_owner(owner)
        else:
            web.ctx.owners.update_owner(owner)
        raise web.seeother('/owners')

class OwnersDeleteHandler:

    def GET(self, id):
        if id == 'all':
            web.ctx.owners.clear()
        else:
            web.ctx.owners.delete_owner(id)
        raise web.seeother('/owners')
