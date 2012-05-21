#!/usr/bin/env python

import web

class IndexHandler:

    def GET(self):
        oracle = {
            'version': web.ctx.oracle.version,
            'username': web.ctx.oracle.username,
            'password': web.ctx.oracle.password,
            'nencoding': web.ctx.oracle.nencoding
        }
        return web.ctx.render.index(oracle)
