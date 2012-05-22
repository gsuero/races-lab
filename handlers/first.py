#!/usr/bin/env python

import web

class FirstHandler:

    def GET(self):
        nickname = web.input(nickname=None).nickname
        if nickname is not None:
            return web.ctx.render.jockeys(web.ctx.jockeys.get_jockeys_by_horse_nickname(nickname))
        return web.ctx.render.first()

