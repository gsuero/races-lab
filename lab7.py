#!/usr/bin/env python

import os

import web
from web.wsgiserver import CherryPyWSGIServer

import cx_Oracle

import handlers.index
import handlers.owners
import handlers.horses

import persistency.owners
import persistency.horses

urls = (
    '/', 'Index',
    '/owners', 'Owners',
    '/owners/new', 'OwnersNew',
    '/owners/update', 'OwnersUpdate',
    '/owners/([a-f0-9]{32})/edit', 'OwnersEdit',
    '/owners/(all|[a-f0-9]{32})/delete', 'OwnersDelete',
    '/horses', 'Horses',
    '/horses/new', 'HorsesNew'
)

# Master-template.
render = web.template.render('templates/', base='layout')

def init_processor(handler):
    # Without this the localized strings are unreadable.
    os.environ["NLS_LANG"] = "RUSSIAN_RUSSIA.UTF8"
    # Connecting to Oracle ...
    web.ctx.oracle = cx_Oracle.connect(open('credentials', 'rt').read())
    web.ctx.oracle.autocommit = True
    web.ctx.owners = persistency.owners.OwnersPersistency(web.ctx.oracle)
    web.ctx.horses = persistency.horses.HorsesPersistency(web.ctx.oracle)
    web.ctx.render = render
    return handler()

if __name__ == "__main__": 
    # Setup HTTPS.
    # CherryPyWSGIServer.ssl_certificate = '../../../../Personal/Keys/eigenein.info.cert'
    # CherryPyWSGIServer.ssl_private_key = '../../../../Personal/Keys/eigenein.info.key'
    # Setup the application handlers.
    app = web.application(urls, {
        'Index': handlers.index.IndexHandler,
        'Owners': handlers.owners.OwnersHandler,
        'OwnersNew': handlers.owners.OwnersNewHandler,
        'OwnersUpdate': handlers.owners.OwnersUpdateHandler,
        'OwnersEdit': handlers.owners.OwnersEditHandler,
        'OwnersDelete': handlers.owners.OwnersDeleteHandler,
        'Horses': handlers.horses.HorsesHandler,
        'HorsesNew': handlers.horses.HorsesNewHandler
    })
    app.add_processor(init_processor)
    # Run.
    app.run()
