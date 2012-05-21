#!/usr/bin/env python

import web

class CompetitionContext:

    def __init__(self):
        self.is_new = True
        self.competition = None

class CompetitionsHandler:

    def GET(self):
        return web.ctx.render.competitions(web.ctx.competitions.get_competitions())

class CompetitionsNewHandler:

    def GET(self):
        competition_context = CompetitionContext()
        competition_context.competition = web.ctx.competitions.create_competition()
        return web.ctx.render.competition(competition_context)

class CompetitionsEditHandler:

    def GET(self, id):
        competition_context = CompetitionContext()
        competition_context.is_new = False
        competition_context.competition = web.ctx.competitions.get_competition(id)
        return web.ctx.render.competition(competition_context)

class CompetitionsUpdateHandler:

    def POST(self):
        user_data = web.input(starts_on='', location = '', title='', races_count = '', id=None)
        competition = web.ctx.competitions.create_competition()
        competition.id = user_data.id
        competition.starts_on = user_data.starts_on
        competition.location = user_data.location
        competition.title = user_data.title
        competition.races_count = user_data.races_count
        if competition.id is None:
            web.ctx.competitions.insert_competition(competition)
        else:
            web.ctx.competitions.update_competition(competition)
        raise web.seeother('/competitions')

class CompetitionsDeleteHandler:

    def GET(self, id):
        if id == 'all':
            web.ctx.competitions.clear()
        else:
            web.ctx.competitions.delete_competition(id)
        raise web.seeother('/competitions')
