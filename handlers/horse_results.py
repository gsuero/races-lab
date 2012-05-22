#!/usr/bin/env python

import web

class HorseResultContext:

    def __init__(self):
        self.is_new = True
        self.horse_result = None
        self.horses = tuple()
        self.competitions = tuple()

class HorseResultsHandler:

    def GET(self):
        return web.ctx.render.horse_results(web.ctx.horse_results.get_horse_results())

class HorseResultsNewHandler:

    def GET(self):
        horse_result_context = HorseResultContext()
        horse_result_context.horse_result = web.ctx.horse_results.create_horse_result()
        horse_result_context.horses = web.ctx.horses.get_horses()
        horse_result_context.competitions = web.ctx.competitions.get_competitions()
        return web.ctx.render.horse_result(horse_result_context)

class HorseResultsEditHandler:

    def GET(self, id):
        competition_id = id[0:32]
        horse_id = id[32:]
        horse_result_context = HorseResultContext()
        horse_result_context.is_new = False
        horse_result_context.horse_result = web.ctx.horse_results.get_horse_result(competition_id, horse_id)
        horse_result_context.horses = web.ctx.horses.get_horses()
        horse_result_context.competitions = web.ctx.competitions.get_competitions()
        return web.ctx.render.horse_result(horse_result_context)

class HorseResultsUpdateHandler:

    def POST(self):
        user_data = web.input(place=1, competition_id=None, horse_id=None, is_new=None)
        horse_result = web.ctx.horse_results.create_horse_result()
        horse_result.competition_id = user_data.competition_id
        horse_result.horse_id = user_data.horse_id
        horse_result.place = int(user_data.place)
        if user_data.is_new:
            web.ctx.horse_results.insert_horse_result(horse_result)
        else:
            web.ctx.horse_results.update_horse_result(horse_result)
        raise web.seeother('/horse_results')

class HorseResultsDeleteHandler:

    def GET(self, id):
        competition_id = id[0:32]
        horse_id = id[32:]
        if competition_id != 'all':
            web.ctx.horse_results.delete_horse_result(competition_id, horse_id)
        else:
            web.ctx.horse_results.clear()
        raise web.seeother('/horse_results')
